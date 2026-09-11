"""Serial stdio MCP tool server; stdout contains protocol messages only."""
import json
import sys

from .handler import Handler
from .validation import ROOT, schema


def loads(text):
    def reject(value):
        raise ValueError('Nonfinite JSON number: ' + value)
    return json.loads(text, parse_constant=reject)


class Server:
    def __init__(self, handler):
        self.handler = handler
        self.initialized = False
        self.ready = False

    def tools(self):
        filename = 'instructions-v0.2.md' if self.handler.version == '0.2' else 'instructions.md'
        instructions = (ROOT / filename).read_text().replace('{max_candidates}', str(self.handler.max_candidates))
        return [
            {'name': 'db_query', 'description': instructions if self.handler.hints else 'Execute one read-only SQLite statement. All database access uses this tool.',
             'inputSchema': schema(self.handler.max_candidates, self.handler.hints, self.handler.version)},
            {'name': 'read_result', 'description': 'Read an archived query result. Use next_offset from the previous response for pagination.',
             'inputSchema': {'type': 'object', 'additionalProperties': False, 'required': ['path'], 'properties': {
                 'path': {'type': 'string'}, 'offset': {'type': 'integer', 'minimum': 0},
                 'limit': {'type': 'integer', 'minimum': 1, 'maximum': 30000}}}},
            {'name': 'submit_answer', 'description': 'Submit the final Markdown report and finish the task.',
             'inputSchema': {'type': 'object', 'additionalProperties': False, 'required': ['markdown'],
                             'properties': {'markdown': {'type': 'string', 'minLength': 1}}}},
        ]

    @staticmethod
    def error(ident, code, message):
        return {'jsonrpc': '2.0', 'id': ident, 'error': {'code': code, 'message': message}}

    def dispatch(self, req):
        if isinstance(req, list):
            if not req:
                return self.error(None, -32600, 'Empty batch')
            responses = [r for item in req if (r := self.dispatch(item)) is not None]
            return responses or None
        if not isinstance(req, dict) or req.get('jsonrpc') != '2.0' or not isinstance(req.get('method'), str):
            return self.error(None, -32600, 'Invalid request')
        ident, method = req.get('id'), req['method']
        if 'id' not in req:
            if method == 'notifications/initialized' and self.initialized:
                self.ready = True
            return None
        params = req.get('params', {})
        if not isinstance(params, dict):
            return self.error(ident, -32602, 'Expected object parameters')
        if method == 'initialize':
            version = params.get('protocolVersion')
            if version not in ('2024-11-05', '2025-03-26'):
                version = '2025-03-26'
            result = {'protocolVersion': version, 'capabilities': {'tools': {}},
                      'serverInfo': {'name': 'agent-db-tool', 'version': self.handler.version+'.0'}}
            self.initialized = True
        elif method == 'ping':
            result = {}
        elif not self.ready:
            return self.error(ident, -32002, 'Initialize and send notifications/initialized first')
        elif method == 'tools/list':
            result = {'tools': self.tools()}
        elif method == 'tools/call':
            name, args = params.get('name'), params.get('arguments', {})
            if name not in {tool['name'] for tool in self.tools()}:
                return self.error(ident, -32602, 'Unknown tool')
            try:
                if name == 'db_query':
                    # MCP RPC IDs belong to the transport session, not durable request IDs.
                    value = self.handler.query(args)
                elif name == 'read_result':
                    if not isinstance(args, dict) or set(args) - {'path', 'offset', 'limit'}:
                        raise ValueError('Invalid read_result arguments')
                    value = self.handler.read_result(**args)
                else:
                    if not isinstance(args, dict) or set(args) != {'markdown'}:
                        raise ValueError('Expected markdown only')
                    value = self.handler.answer(args['markdown'])
                failed = value.get('status', 'ok') != 'ok'
            except (ValueError, TypeError, OSError) as exc:
                value, failed = {'error': f'{type(exc).__name__}: {exc}'}, True
            result = {'content': [{'type': 'text', 'text': json.dumps(value, ensure_ascii=False)}], 'isError': failed}
        else:
            return self.error(ident, -32601, 'Method not found')
        return {'jsonrpc': '2.0', 'id': ident, 'result': result}

    def serve(self):
        try:
            for line in sys.stdin:
                try:
                    req = loads(line)
                except (ValueError, UnicodeError):
                    response = self.error(None, -32700, 'Invalid JSON')
                else:
                    response = self.dispatch(req)
                if response is not None:
                    print(json.dumps(response, ensure_ascii=False), flush=True)
        finally:
            self.handler.close()

import argparse
import json
from pathlib import Path

from .dacomp import prepare
from .handler import Handler
from .server import Server, loads
from .validation import schema


def main():
    parser = argparse.ArgumentParser(description='Agent SQL + future-access tool')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare-dacomp')
    p.add_argument('--task', required=True)
    p.add_argument('--run', required=True)
    p.add_argument('--benchmark', default=str(Path(__file__).resolve().parents[1] / 'benchmark/dacomp'))
    p.add_argument('--mode', choices=['hints', 'sql-only'], default='hints')
    p.add_argument('--max-candidates', type=int, default=8)
    p.add_argument('--schema-version', choices=['0.1', '0.2'], default='0.2')
    p = sub.add_parser('serve')
    p.add_argument('--run', required=True)
    p = sub.add_parser('query')
    p.add_argument('--run', required=True)
    p.add_argument('--request-file', required=True)
    p.add_argument('--request-id')
    p = sub.add_parser('schema')
    p.add_argument('--schema-version', choices=['0.1', '0.2'], default='0.2')
    args = parser.parse_args()
    if args.command == 'prepare-dacomp':
        result = prepare(args.task, args.run, args.benchmark, args.mode, args.max_candidates, args.schema_version)
        print(json.dumps({'prepared': str(Path(args.run).resolve()), 'task_id': result['task_id'], 'mode': result['mode']}))
    elif args.command == 'serve':
        Server(Handler(args.run)).serve()
    elif args.command == 'query':
        value = loads(Path(args.request_file).read_text())
        handler = Handler(args.run)
        try:
            print(json.dumps(handler.query(value, args.request_id), ensure_ascii=False))
        finally:
            handler.close()
    else:
        print(json.dumps(schema(version=args.schema_version), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

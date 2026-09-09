import json
with open('/results/S34.rows.jsonl') as f:
    line = f.readline()
    print(repr(line[:500]))
    obj = json.loads(line)
    print(type(obj))
    if isinstance(obj, dict):
        print(list(obj.keys()))
    else:
        print(obj[:2])
import json, re
from datetime import datetime

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query3/full-01/results/f9911c253a644f3ab975cb7bc09b716d.json"
rows = json.load(open(path))
print("rows:", len(rows))

formats = [
    "%Y-%m-%d %H:%M:%S",
    "%d %b %Y, %H:%M",
    "%B %d, %Y at %I:%M %p",
]

def parse(s):
    s = s.strip()
    for f in formats:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None

bad = []
biz2018 = set()
for r in rows:
    d = parse(r["date"])
    if d is None:
        bad.append(r["date"])
        continue
    if d.year == 2018:
        biz2018.add(r["business_ref"])

print("unparsed:", len(bad), set(bad) if bad else "")
print("distinct businesses with >=1 review in 2018:", len(biz2018))
print(sorted(biz2018, key=lambda x: int(x.split("_")[1])))

# compare with earlier LIKE-based set
old = {"businessref_59","businessref_67","businessref_15","businessref_13","businessref_24","businessref_79","businessref_91","businessref_66","businessref_99","businessref_25","businessref_36","businessref_46","businessref_17","businessref_47","businessref_73","businessref_43","businessref_77","businessref_26","businessref_86","businessref_40","businessref_62","businessref_20","businessref_82","businessref_83","businessref_35","businessref_45","businessref_22","businessref_8","businessref_80","businessref_14","businessref_28","businessref_57","businessref_4","businessref_37","businessref_68","businessref_27"}
print("new not in old:", sorted(biz2018 - old))
print("old not in new:", sorted(old - biz2018))

import json, re
from collections import defaultdict

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/f00079fe297e4114a2943386d14643e7.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/0197c66f295c4ca49c138a8b1afc4d04.json"))

year_re = re.compile(r'\b(1[89]\d{2}|20[0-2]\d)\b')

# find books with multiple distinct years
for b in books:
    ys = year_re.findall(b["details"] or "")
    if len(set(ys)) > 1:
        print(b["book_id"], set(ys), "||", (b["details"] or "")[:200])

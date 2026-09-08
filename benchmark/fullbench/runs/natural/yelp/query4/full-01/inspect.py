import json

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/604e6e7e916d4e7abcb7e2ce011c42d0.json"
biz = json.load(open(biz_file))
names = ['The Recovery Room Bar & Grill', 'The Iron Shop', 'The Jungle', "Pat Flynn's Public House", 'Taste of Europe', 'Fox and Hound English Pub and Grille', 'Salt + Smoke', 'Avian Glen Winery']
for b in biz:
    if b["name"] in names:
        print(b["name"], "||", b["description"])
        print()

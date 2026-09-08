import json

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query3/full-01/results/bdfcbac20da94e3aab1da45299458362.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query3/full-01/results/186ef193e915489085bf787d02963642.json"))

# map purchase_id numeric suffix -> review stats
rev_map = {int(r["purchase_id"].split("_")[1]): r for r in reviews}

results = []
for b in books:
    n = int(b["book_id"].split("_")[1])
    if n in rev_map:
        results.append((b["title"], b["book_id"], rev_map[n]["avg_rating"], rev_map[n]["num_reviews"]))

results.sort(key=lambda x: (-x[2], x[0]))
for title, bid, avg, cnt in results:
    print(f"{title} | {bid} | avg={avg:.4f} | reviews={cnt}")
print("TOTAL:", len(results))

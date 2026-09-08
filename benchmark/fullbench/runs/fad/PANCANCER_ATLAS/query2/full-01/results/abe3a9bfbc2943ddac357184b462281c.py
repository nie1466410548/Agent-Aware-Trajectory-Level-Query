import json

clin_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query2/full-01/results/d26814ac52d94904b89d408404365116.json"
mut_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query2/full-01/results/5ec52f82a75d467bac9cbacb92d27292.json"

clin = json.load(open(clin_path))
mut = json.load(open(mut_path))

cdh1 = set(r["ParticipantBarcode"] for r in mut)

from collections import defaultdict
total = defaultdict(int)
mutated = defaultdict(int)
for r in clin:
    ht = r["histological_type"]
    total[ht] += 1
    if r["barcode"] in cdh1:
        mutated[ht] += 1

rows = []
for ht, n in total.items():
    m = mutated.get(ht, 0)
    rows.append((ht, n, m, 100.0 * m / n))

rows.sort(key=lambda x: -x[3])
print(f"{'histological_type':40s} {'alive_total':>11s} {'cdh1_mut':>8s} {'pct':>8s}")
for ht, n, m, pct in rows:
    print(f"{str(ht):40s} {n:11d} {m:8d} {pct:7.2f}%")

print("\nTotal alive BRCA patients:", len(clin))
print("Unique barcodes:", len(set(r['barcode'] for r in clin)))
print("Null barcode rows:", sum(1 for r in clin if not r['barcode']))

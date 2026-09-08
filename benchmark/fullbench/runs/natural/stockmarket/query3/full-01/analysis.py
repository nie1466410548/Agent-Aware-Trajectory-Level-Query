import json, re

info = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query3/full-01/results/ac7e2a69960e4f2aaf634d4f3bbcd063.json'))
vols = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query3/full-01/results/eafb4ee7f84b479c9ef8f95f325fd816.json'))

meta = {r['Symbol']: r for r in info}

# Extract a concise company name from the description (text before the first verb phrase)
def name_of(desc):
    m = re.split(r'\s+(?:specializes|is|provides|harnesses|based|offers|dedicated|focuses|transforming)\b', desc, maxsplit=1)
    return m[0].strip().rstrip(',')

rows = []
for r in vols:
    if r['days_2008'] > 0 and r['avg_volume_2008'] is not None:
        sym = r['symbol']
        rows.append((name_of(meta[sym]['Company Description']), sym, meta[sym]['Financial Status'], r['avg_volume_2008']))

rows.sort(key=lambda x: x[0])
lines = ["NASDAQ-listed financially troubled companies (delinquent/deficient) with 2008 trading volume:",
         ""]
for name, sym, fs, avg in rows:
    lines.append(f"{name} ({sym}, Financial Status: {fs}): average daily trading volume in 2008 = {avg:.2f} shares ({int(round(avg))} shares approx.)")
lines.append("")
lines.append(f"Total: {len(rows)} companies (of 25 financially troubled NASDAQ-listed securities, the rest had no 2008 trading data).")
open('final.txt','w').write("\n".join(lines))
print("\n".join(lines))

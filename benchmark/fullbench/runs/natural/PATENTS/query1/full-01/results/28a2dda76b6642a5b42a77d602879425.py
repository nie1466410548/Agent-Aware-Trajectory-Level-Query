import json
import pandas as pd

COUNTS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query1/full-01/results/960b572783834a45a1ffda3046245e1e.json"
LEVEL5 = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query1/full-01/results/7de1a1ef05664a21aeb1cc0a80a1423a.json"

with open(COUNTS) as f:
    counts = pd.DataFrame(json.load(f))
with open(LEVEL5) as f:
    lvl5 = {r["symbol"] for r in json.load(f)}

print("count rows:", len(counts), "| distinct subs in counts:", counts["sub"].nunique())
print("level-5 symbols:", len(lvl5))

# Keep only CPC group codes that exist at level 5 in the definition database
df = counts[counts["sub"].isin(lvl5)].copy()
print("subs matched to level5:", df["sub"].nunique())

years = list(range(df["yr"].min(), df["yr"].max() + 1))
print("year range:", years[0], "-", years[-1])

piv = df.pivot_table(index="sub", columns="yr", values="cnt", aggfunc="sum")
piv = piv.reindex(columns=years, fill_value=0).fillna(0).sort_index()

# Exponential moving average with smoothing factor alpha = 0.2
ema = piv.T.ewm(alpha=0.2, adjust=False).mean().T  # rows: sub, cols: year

best_year = ema.idxmax(axis=1)
res = best_year[best_year == 2022].sort_index()

print("\nBest-year distribution (top):")
print(best_year.value_counts().sort_index().to_string())

print("\nLevel-5 CPC codes whose best year is 2022 (%d):" % len(res))
for s in res.index:
    print(s, "| EMA2022=%.3f" % ema.loc[s, 2022], "| counts 2020-2024:",
          [int(piv.loc[s, y]) for y in range(2020, 2025)])

with open("answer_codes.txt", "w") as f:
    f.write("\n".join(res.index))

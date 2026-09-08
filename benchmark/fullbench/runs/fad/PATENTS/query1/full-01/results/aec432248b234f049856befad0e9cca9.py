import json
import pandas as pd

COUNTS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query1/full-01/results/a35028c05c3d48d990e8729ea7decdb3.json"
LEVEL5 = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query1/full-01/results/f07147bb9bc7448cbfba90888ef75193.json"

counts = pd.DataFrame(json.load(open(COUNTS)))
lvl5 = set(r["symbol"] for r in json.load(open(LEVEL5)))
print("level-5 symbols:", len(lvl5))
print("distinct subclasses in counts:", counts["subclass"].nunique())
missing = sorted(set(counts["subclass"]) - lvl5)
print("subclasses not in level-5 def (dropped):", missing)

df = counts[counts["subclass"].isin(lvl5)].copy()
ymin, ymax = int(df["yr"].min()), int(df["yr"].max())
print("year range:", ymin, ymax)

piv = df.pivot_table(index="subclass", columns="yr", values="n", aggfunc="sum").fillna(0)
piv = piv.reindex(columns=range(ymin, ymax + 1), fill_value=0).sort_index()

def per_year_winners(ema):
    out = {}
    for y in ema.columns:
        out[y] = ema[y].idxmax()
    return out

# Variant 1: full zero-filled grid, adjust=False (standard EMA recursion, alpha=0.2)
ema1 = piv.T.ewm(alpha=0.2, adjust=False).mean().T
w1 = per_year_winners(ema1)
print("\nVariant 1 (full grid, adjust=False): recent winners:")
for y in range(2015, ymax + 1):
    top = ema1[y].nlargest(3)
    print(y, list(top.items()))
print("2022 winner:", w1[2022])

# Variant 2: series starts at each subclass's first observed year (leading NaNs dropped)
ema2 = piv.T.ewm(alpha=0.2, adjust=False, ignore_na=True).mean().T
# emulate fresh-start: compute per subclass only from first nonzero year
def ema_fresh(s):
    nz = s[s > 0]
    if len(nz) == 0:
        return s * 0
    first = nz.index[0]
    sub = s.loc[first:]
    e = sub.ewm(alpha=0.2, adjust=False).mean()
    return s * 0 + e.reindex(s.index).fillna(0)
ema2 = piv.apply(ema_fresh, axis=1)
w2 = per_year_winners(ema2)
print("\nVariant 2 (fresh start at first filing): 2022 winner:", w2[2022])
top = ema2[2022].nlargest(3); print(list(top.items()))

# Variant 3: adjust=True on full grid
ema3 = piv.T.ewm(alpha=0.2, adjust=True).mean().T
w3 = per_year_winners(ema3)
print("\nVariant 3 (full grid, adjust=True): 2022 winner:", w3[2022])
top = ema3[2022].nlargest(3); print(list(top.items()))

# Alternative reading: per-subclass best (max EMA) year == 2022
best_year_v1 = ema1.idxmax(axis=1)
by2022 = sorted(best_year_v1[best_year_v1 == 2022].index)
print("\nAlt reading: subclasses whose max-EMA year is 2022 (variant1):", len(by2022), by2022[:20])

# All winners per year for context (variant 1)
print("\nAll yearly winners (variant 1):")
for y in sorted(w1):
    print(y, w1[y], round(ema1.loc[w1[y], y], 2))

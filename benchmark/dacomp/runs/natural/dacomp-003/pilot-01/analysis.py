import json
import pandas as pd
import numpy as np
from scipy import stats

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-003/pilot-01/results/970b2031ecca4a52a6a4fa7e64c4385d.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["ind_share"] = df["ind_wc"] / df["tot_wc"] * 100

print("Regions:", sorted(df.rname.unique()))
print("Rows:", len(df))
print("Missing values:\n", df.isna().sum())

# ---- China overall (time series) ----
cn = df[df.rcode == 142].sort_values("yr").copy()
print("\n=== China overall (rcode 142) ===")
print(cn[["yr", "gdp_pc", "ind_wc", "tot_wc", "ind_share"]].to_string(index=False))

# Spearman & Pearson between ind_share and gdp_pc over time
r_p, p_p = stats.pearsonr(cn.gdp_pc, cn.ind_share)
r_s, p_s = stats.spearmanr(cn.gdp_pc, cn.ind_share)
print(f"\nPearson r(share, gdp_pc) = {r_p:.3f} (p={p_p:.4f})")
print(f"Spearman rho(share, gdp_pc) = {r_s:.3f} (p={p_s:.4f})")

# Piecewise: before/after peak of share
peak_idx = cn.ind_share.idxmax()
print("Share peak year:", cn.loc[peak_idx, "yr"], "share:", cn.loc[peak_idx, "ind_share"])
early = cn[cn.yr <= cn.loc[peak_idx, "yr"]]
late = cn[cn.yr >= cn.loc[peak_idx, "yr"]]
for name, sub in [("rising phase", early), ("declining phase", late)]:
    rs, ps = stats.spearmanr(sub.gdp_pc, sub.ind_share)
    print(f"  {name}: n={len(sub)}, spearman={rs:.3f}, p={ps:.4f}")

# ---- Province-level time-series correlations ----
prov = df[df.rcode != 142].copy()
rows = []
for rname, g in prov.groupby("rname"):
    g = g.dropna(subset=["gdp_pc", "ind_share"])
    if len(g) >= 5:
        rs, ps = stats.spearmanr(g.gdp_pc, g.ind_share)
        rp, pp = stats.pearsonr(g.gdp_pc, g.ind_share)
        rows.append({"region": rname, "n": len(g), "spearman": rs, "p_spearman": ps,
                     "pearson": rp, "share_first": g.sort_values("yr").ind_share.iloc[0],
                     "share_last": g.sort_values("yr").ind_share.iloc[-1],
                     "gdp_first": g.sort_values("yr").gdp_pc.iloc[0],
                     "gdp_last": g.sort_values("yr").gdp_pc.iloc[-1]})
corr = pd.DataFrame(rows).sort_values("spearman")
print("\n=== Per-region time-series Spearman corr(ind_share, gdp_pc) ===")
print(corr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
corr.to_csv("region_corrs.csv", index=False)

# ---- Cross-sectional analysis (pooled and by year) ----
print("\n=== Cross-sectional Spearman corr by year (provinces only) ===")
cs = []
for yr, g in prov.groupby("yr"):
    g = g.dropna(subset=["gdp_pc", "ind_share"])
    if len(g) >= 10:
        rs, ps = stats.spearmanr(g.gdp_pc, g.ind_share)
        cs.append({"year": yr, "n": len(g), "spearman": rs, "p": ps})
cs = pd.DataFrame(cs)
print(cs.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
cs.to_csv("cross_section.csv", index=False)

# Pooled
gp = prov.dropna(subset=["gdp_pc", "ind_share"])
rs, ps = stats.spearmanr(gp.gdp_pc, gp.ind_share)
print(f"\nPooled provincial spearman: {rs:.3f}, p={ps:.2e}, n={len(gp)}")

# log-gdp version
gp2 = gp[gp.gdp_pc > 0]
rs, ps = stats.spearmanr(np.log(gp2.gdp_pc), gp2.ind_share)
print(f"Pooled spearman(log gdp): {rs:.3f}")

# group regions by relationship type
neg = corr[corr.spearman < -0.5]
pos = corr[corr.spearman > 0.5]
mid = corr[(corr.spearman >= -0.5) & (corr.spearman <= 0.5)]
print("\nStrong negative (decoupling):", list(neg.region))
print("Strong positive:", list(pos.region))
print("Weak/mixed:", list(mid.region))

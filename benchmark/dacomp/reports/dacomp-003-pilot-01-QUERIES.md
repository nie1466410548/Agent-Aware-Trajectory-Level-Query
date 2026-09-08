# dacomp-003 / pilot-01 查询与 Python 清单

Q 编号按该任务 SQL 尝试的开始时间排序，包含错误和元数据查询；P 编号独立。不同任务的 Q 编号不相关。

GROUP BY 仅为语法清单，不等于跨查询下钻或复用机会。CTE 名称可能出现在表名清单中。

## 工具时间顺序

list-db → Q1 → Q2 → P1 → P2 → P3 → answer

SQL 结果文件在后续 Python 源码中的引用：Q2 → P1；Q2 → P2；Q2 → P3

## Q1 — 成功

结果行数：1；执行并取回：0.369 ms；元数据：False

```sql
SELECT MIN("Year") AS min_year, MAX("Year") AS max_year, COUNT(*) AS n_rows, COUNT(DISTINCT "Region Code") AS n_regions
FROM sheet1;

```

[完整结果](../runs/natural/dacomp-003/pilot-01/results/6c47b63d36c840d5a08c4b308bedccc2.json)

## Q2 — 成功

结果行数：515；执行并取回：2.501 ms；元数据：False

```sql
SELECT e."Year" AS yr, e."Region Code" AS rcode, e."Region Name" AS rname,
e."Per capita GDP (yuan/person)" AS gdp_pc,
s."Industrial Water Consumption (100 million m³)" AS ind_wc,
s."Total Water Consumption (100 million m³) " AS tot_wc,
e."Urbanization rate (%)" AS urb,
e."Industrial value added (100 million yuan)" AS iva
FROM economic_indicator_data e
JOIN sheet1 s ON e."Year" = s."Year" AND e."Region Code" = s."Region Code"
ORDER BY rcode, yr;

```

[完整结果](../runs/natural/dacomp-003/pilot-01/results/970b2031ecca4a52a6a4fa7e64c4385d.json)

## P1 — Python 成功

```python
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

```

[完整 stdout/stderr](../runs/natural/dacomp-003/pilot-01/results/8c448706f329431b9a77a29289cc442b.json)

## P2 — Python 失败

```python
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-003/pilot-01/results/970b2031ecca4a52a6a4fa7e64c4385d.json") as f:
    df = pd.DataFrame(json.load(f))
df["ind_share"] = df["ind_wc"] / df["tot_wc"] * 100
cn = df[df.rcode == 142].sort_values("yr").copy()
prov = df[df.rcode != 142].copy()

# ---- Fig 1: China overall time series ----
fig, ax1 = plt.subplots(figsize=(8, 4.8))
ax1.plot(cn.yr, cn.ind_share, "o-", color="tab:blue", label="Industrial water share (%)")
ax1.axvline(2007, ls="--", color="grey", lw=1)
ax1.text(2007.2, ax1.get_ylim()[0]+0.5, "peak 2007", fontsize=9, color="grey")
ax1.set_xlabel("Year"); ax1.set_ylabel("Industrial share of total water use (%)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax2 = ax1.twinx()
ax2.plot(cn.yr, cn.gdp_pc, "s--", color="tab:red", label="Per-capita GDP (yuan)")
ax2.set_ylabel("Per-capita GDP (yuan/person)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax1.set_title("China overall: industrial water share vs economic development, 2000-2018")
fig.tight_layout(); fig.savefig("fig1_china_overall.png", dpi=150); plt.close(fig)

# ---- Fig 2: China scatter share vs GDP, colored by year ----
fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.scatter(cn.gdp_pc, cn.ind_share, c=cn.yr, cmap="viridis", s=60)
for _, r in cn.iterrows():
    if r.yr in (2000, 2007, 2011, 2018):
        ax.annotate(int(r.yr), (r.gdp_pc, r.ind_share), textcoords="offset points",
                    xytext=(6, 4), fontsize=9)
ax.plot(cn.sort_values("yr").gdp_pc, cn.sort_values("yr").ind_share, color="grey", alpha=0.4, lw=1)
fig.colorbar(sc, label="Year")
ax.set_xlabel("Per-capita GDP (yuan/person)")
ax.set_ylabel("Industrial share of total water use (%)")
ax.set_title("China: inverted-U (EKC-type) path of industrial water share")
fig.tight_layout(); fig.savefig("fig2_china_scatter.png", dpi=150); plt.close(fig)

# ---- Fig 3: Cross-sectional scatter 2003 vs 2018 ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for ax, yr in zip(axes, [2003, 2018]):
    g = prov[prov.yr == yr]
    ax.scatter(g.gdp_pc, g.ind_share, s=45, color="tab:green", alpha=0.8)
    # label a few extremes
    for _, r in g.iterrows():
        if r.ind_share > 40 or r.ind_share < 4 or r.gdp_pc > 45000:
            ax.annotate(r.rname.replace(" Province", "").replace(" Municipality", "")
                        .replace(" Autonomous Region", "").replace(" Zhuang", "").replace(" Uygur", "").replace(" Hui", ""),
                        (r.gdp_pc, r.ind_share), textcoords="offset points", xytext=(4, 4), fontsize=7)
    m, b = np.polyfit(g.gdp_pc, g.ind_share, 1)
    xs = np.linspace(g.gdp_pc.min(), g.gdp_pc.max(), 50)
    ax.plot(xs, m*xs + b, ls="--", color="darkgreen")
    ax.set_title(f"Cross-section {yr} (n={len(g)})")
    ax.set_xlabel("Per-capita GDP (yuan/person)")
axes[0].set_ylabel("Industrial share of total water use (%)")
fig.suptitle("Across provinces within a year: richer provinces show higher industrial water share")
fig.tight_layout(); fig.savefig("fig3_cross_section.png", dpi=150); plt.close(fig)

# ---- Fig 4: bar chart of per-region spearman correlations ----
corr = pd.read_csv("region_corrs.csv").sort_values("spearman")
fig, ax = plt.subplots(figsize=(9, 8))
colors = ["tab:red" if v < -0.5 else ("tab:blue" if v > 0.5 else "grey") for v in corr.spearman]
names = [n.replace(" Province", "").replace(" Municipality", "").replace(" Autonomous Region", "")
         .replace(" Zhuang", "").replace(" Uygur", "").replace(" Hui", "") for n in corr.region]
ax.barh(names, corr.spearman, color=colors)
ax.axvline(-0.5, ls=":", color="tab:red"); ax.axvline(0.5, ls=":", color="tab.blue")
ax.set_xlabel("Spearman correlation: industrial water share vs per-capita GDP (2003-2018)")
ax.set_title("Within-region relationship differs strongly across provinces")
for i, (v, p) in enumerate(zip(corr.spearman, corr.p_spearman)):
    ax.text(v + (0.02 if v >= 0 else -0.02), i, f"{v:.2f}" + ("*" if p < 0.05 else ""),
            va="center", ha="left" if v >= 0 else "right", fontsize=8)
fig.tight_layout(); fig.savefig("fig4_region_corrs.png", dpi=150); plt.close(fig)

# ---- Fig 5: trajectories of representative regions ----
fig, ax = plt.subplots(figsize=(8.5, 5.5))
picks = {"Beijing Municipality": "tab:red", "Shanghai Municipality": "tab:orange",
         "Guangdong Province": "tab:purple", "Jiangsu Province": "tab:blue",
         "Ningxia Hui Autonomous Region": "tab:green", "Xinjiang Uygur Autonomous Region": "tab:brown"}
for name, c in picks.items():
    g = prov[prov.rname == name].sort_values("yr")
    ax.plot(g.gdp_pc, g.ind_share, "o-", color=c, ms=4, lw=1.4,
            label=name.replace(" Municipality", "").replace(" Province", "").replace(" Hui Autonomous Region", "").replace(" Uygur Autonomous Region", ""))
    ax.annotate(int(g.yr.iloc[0]), (g.gdp_pc.iloc[0], g.ind_share.iloc[0]), fontsize=7,
                textcoords="offset points", xytext=(4, -8), color=c)
    ax.annotate(int(g.yr.iloc[-1]), (g.gdp_pc.iloc[-1], g.ind_share.iloc[-1]), fontsize=7,
                textcoords="offset points", xytext=(4, 4), color=c)
ax.set_xlabel("Per-capita GDP (yuan/person)")
ax.set_ylabel("Industrial share of total water use (%)")
ax.set_title("Selected provincial trajectories, 2003-2018 (labels = first/last year)")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig("fig5_trajectories.png", dpi=150); plt.close(fig)

print("done")

```

[完整 stdout/stderr](../runs/natural/dacomp-003/pilot-01/results/967efbcdde774ce9a8740d5830de3b32.json)

## P3 — Python 成功

```python
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-003/pilot-01/results/970b2031ecca4a52a6a4fa7e64c4385d.json") as f:
    df = pd.DataFrame(json.load(f))
df["ind_share"] = df["ind_wc"] / df["tot_wc"] * 100
cn = df[df.rcode == 142].sort_values("yr").copy()
prov = df[df.rcode != 142].copy()

# ---- Fig 1: China overall time series ----
fig, ax1 = plt.subplots(figsize=(8, 4.8))
ax1.plot(cn.yr, cn.ind_share, "o-", color="tab:blue", label="Industrial water share (%)")
ax1.axvline(2007, ls="--", color="grey", lw=1)
ax1.text(2007.2, ax1.get_ylim()[0]+0.5, "peak 2007", fontsize=9, color="grey")
ax1.set_xlabel("Year"); ax1.set_ylabel("Industrial share of total water use (%)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax2 = ax1.twinx()
ax2.plot(cn.yr, cn.gdp_pc, "s--", color="tab:red", label="Per-capita GDP (yuan)")
ax2.set_ylabel("Per-capita GDP (yuan/person)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax1.set_title("China overall: industrial water share vs economic development, 2000-2018")
fig.tight_layout(); fig.savefig("fig1_china_overall.png", dpi=150); plt.close(fig)

# ---- Fig 2: China scatter share vs GDP, colored by year ----
fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.scatter(cn.gdp_pc, cn.ind_share, c=cn.yr, cmap="viridis", s=60)
for _, r in cn.iterrows():
    if r.yr in (2000, 2007, 2011, 2018):
        ax.annotate(int(r.yr), (r.gdp_pc, r.ind_share), textcoords="offset points",
                    xytext=(6, 4), fontsize=9)
ax.plot(cn.sort_values("yr").gdp_pc, cn.sort_values("yr").ind_share, color="grey", alpha=0.4, lw=1)
fig.colorbar(sc, label="Year")
ax.set_xlabel("Per-capita GDP (yuan/person)")
ax.set_ylabel("Industrial share of total water use (%)")
ax.set_title("China: inverted-U (EKC-type) path of industrial water share")
fig.tight_layout(); fig.savefig("fig2_china_scatter.png", dpi=150); plt.close(fig)

# ---- Fig 3: Cross-sectional scatter 2003 vs 2018 ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for ax, yr in zip(axes, [2003, 2018]):
    g = prov[prov.yr == yr]
    ax.scatter(g.gdp_pc, g.ind_share, s=45, color="tab:green", alpha=0.8)
    # label a few extremes
    for _, r in g.iterrows():
        if r.ind_share > 40 or r.ind_share < 4 or r.gdp_pc > 45000:
            ax.annotate(r.rname.replace(" Province", "").replace(" Municipality", "")
                        .replace(" Autonomous Region", "").replace(" Zhuang", "").replace(" Uygur", "").replace(" Hui", ""),
                        (r.gdp_pc, r.ind_share), textcoords="offset points", xytext=(4, 4), fontsize=7)
    m, b = np.polyfit(g.gdp_pc, g.ind_share, 1)
    xs = np.linspace(g.gdp_pc.min(), g.gdp_pc.max(), 50)
    ax.plot(xs, m*xs + b, ls="--", color="darkgreen")
    ax.set_title(f"Cross-section {yr} (n={len(g)})")
    ax.set_xlabel("Per-capita GDP (yuan/person)")
axes[0].set_ylabel("Industrial share of total water use (%)")
fig.suptitle("Across provinces within a year: richer provinces show higher industrial water share")
fig.tight_layout(); fig.savefig("fig3_cross_section.png", dpi=150); plt.close(fig)

# ---- Fig 4: bar chart of per-region spearman correlations ----
corr = pd.read_csv("region_corrs.csv").sort_values("spearman")
fig, ax = plt.subplots(figsize=(9, 8))
colors = ["tab:red" if v < -0.5 else ("tab:blue" if v > 0.5 else "grey") for v in corr.spearman]
names = [n.replace(" Province", "").replace(" Municipality", "").replace(" Autonomous Region", "")
         .replace(" Zhuang", "").replace(" Uygur", "").replace(" Hui", "") for n in corr.region]
ax.barh(names, corr.spearman, color=colors)
ax.axvline(-0.5, ls=":", color="tab:red"); ax.axvline(0.5, ls=":", color="tab:blue")
ax.set_xlabel("Spearman correlation: industrial water share vs per-capita GDP (2003-2018)")
ax.set_title("Within-region relationship differs strongly across provinces")
for i, (v, p) in enumerate(zip(corr.spearman, corr.p_spearman)):
    ax.text(v + (0.02 if v >= 0 else -0.02), i, f"{v:.2f}" + ("*" if p < 0.05 else ""),
            va="center", ha="left" if v >= 0 else "right", fontsize=8)
fig.tight_layout(); fig.savefig("fig4_region_corrs.png", dpi=150); plt.close(fig)

# ---- Fig 5: trajectories of representative regions ----
fig, ax = plt.subplots(figsize=(8.5, 5.5))
picks = {"Beijing Municipality": "tab:red", "Shanghai Municipality": "tab:orange",
         "Guangdong Province": "tab:purple", "Jiangsu Province": "tab:blue",
         "Ningxia Hui Autonomous Region": "tab:green", "Xinjiang Uygur Autonomous Region": "tab:brown"}
for name, c in picks.items():
    g = prov[prov.rname == name].sort_values("yr")
    ax.plot(g.gdp_pc, g.ind_share, "o-", color=c, ms=4, lw=1.4,
            label=name.replace(" Municipality", "").replace(" Province", "").replace(" Hui Autonomous Region", "").replace(" Uygur Autonomous Region", ""))
    ax.annotate(int(g.yr.iloc[0]), (g.gdp_pc.iloc[0], g.ind_share.iloc[0]), fontsize=7,
                textcoords="offset points", xytext=(4, -8), color=c)
    ax.annotate(int(g.yr.iloc[-1]), (g.gdp_pc.iloc[-1], g.ind_share.iloc[-1]), fontsize=7,
                textcoords="offset points", xytext=(4, 4), color=c)
ax.set_xlabel("Per-capita GDP (yuan/person)")
ax.set_ylabel("Industrial share of total water use (%)")
ax.set_title("Selected provincial trajectories, 2003-2018 (labels = first/last year)")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig("fig5_trajectories.png", dpi=150); plt.close(fig)

print("done")

```

[完整 stdout/stderr](../runs/natural/dacomp-003/pilot-01/results/59e307eb7fbc477494cae9b99dfe08c7.json)

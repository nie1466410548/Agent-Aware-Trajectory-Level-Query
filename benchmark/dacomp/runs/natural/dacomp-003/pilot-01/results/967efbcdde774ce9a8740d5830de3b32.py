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

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Data from S33
data = [
 ["Department Store",64,1.6755,2.531,1692.9,47.11,0.8478,19.7,15.57,812783.0,25399.5,63,45140.0,716.5,0.547,0.375,0.391,0.3125,0.9708,32.08,0.515625],
 ["Food Store",63,1.632,2.703,681.8,48.22,0.8465,8.56,19.39,624432.0,20143.0,63,42460.0,674.0,0.46,0.349,0.317,0.3016,0.9766,32.66,0.50794],
 ["Restaurant",62,1.6164,2.257,734.1,47.15,0.8194,16.13,8.68,1089042.0,30251.2,62,41960.0,676.8,0.468,0.339,0.29,0.2903,0.9755,32.55,0.5],
 ["Gas station",60,1.6031,2.633,804.7,47.27,0.8467,19.57,14.91,1117258.0,31034.9,60,40000.0,666.7,0.483,0.333,0.333,0.25,0.9787,32.87,0.41667],
 ["Supermarket",59,1.5864,2.949,1567.4,46.27,0.8223,24.32,18.27,668702.0,22290.1,59,39260.0,665.4,0.458,0.407,0.271,0.2373,0.9724,32.24,0.44068],
 ["Shopping Center",58,1.529,2.68,1510.9,52.43,0.8418,11.02,12.91,583542.0,26524.6,57,42060.0,737.9,0.534,0.259,0.328,0.3448,0.9778,32.78,0.5],
 ["Retail Store",57,1.5206,2.183,636.8,55.81,0.8264,11.75,6.94,713517.0,25482.8,56,37920.0,677.1,0.526,0.263,0.421,0.3860,0.9793,32.93,0.43860],
 ["Specialty store",55,1.6459,2.869,1627.2,48.82,0.8615,13.96,7.76,960110.0,29094.2,55,30640.0,557.1,0.673,0.473,0.236,0.3636,0.9752,32.52,0.27273],
 ["Convenience Store",53,1.699,2.088,718.1,51.3,0.8363,18.51,19.78,841028.0,31149.2,51,37000.0,725.5,0.528,0.302,0.396,0.3585,0.9727,32.27,0.49057],
 ["Beverage Shop",52,1.565,2.494,692.7,45.0,0.8071,13.72,14.54,652482.0,31070.6,51,32420.0,635.7,0.423,0.333,0.333,0.4510,0.9818,33.18,0.5],
]
cols = ["Outlet Type","num_outlets","pos_target_ach","avg_vpo","avg_pc","avg_qual_rate",
        "avg_tar","avg_yoy","avg_mom","total_sales_value","avg_sales_value",
        "num_contracts","total_signing_amount","avg_signing_amount","renewal_ratio",
        "complaint_ratio","quality_ratio","renew_high_ratio","avg_pass_rate","avg_score","appeals_per_outlet"]
df = pd.DataFrame(data, columns=cols)

# Compute composite scores
def pct_rank(s):
    return 100 * (s.rank(pct=True))

df["perf_score"] = (pct_rank(df["avg_tar"])*0.35 + pct_rank(df["pos_target_ach"])*0.25 + 
                     pct_rank(df["avg_yoy"])*0.20 + pct_rank(df["avg_sales_value"])*0.20)
df["risk_score"] = (pct_rank(df["complaint_ratio"])*0.40 + pct_rank(df["quality_ratio"])*0.25 + 
                     pct_rank(df["appeals_per_outlet"])*0.20 + (100 - pct_rank(df["renewal_ratio"]))*0.15)
df["health_score"] = (pct_rank(df["renewal_ratio"])*0.45 + pct_rank(df["renew_high_ratio"])*0.30 + 
                       pct_rank(df["avg_pass_rate"])*0.15 + pct_rank(df["avg_score"])*0.10)

# Recommendation: 
# net_score = perf_score - risk_score (higher = better candidate for increase)
df["net_score"] = df["perf_score"] - df["risk_score"]
df["recommendation"] = pd.cut(df["net_score"], bins=[-float('inf'), -15, 15, float('inf')], 
                               labels=["Reduce", "Maintain", "Increase"])

# Sort by net score
df = df.sort_values("net_score", ascending=False)

print("=== Final Recommendation Ranking ===")
print(df[["Outlet Type","perf_score","risk_score","health_score","net_score","recommendation"]].round(1).to_string(index=False))

# --- FIGURE 1: Performance vs Risk Scatter (Bubble Chart) ---
fig, ax = plt.subplots(figsize=(12, 8))
colors = {"Increase": "#2ecc71", "Maintain": "#f39c12", "Reduce": "#e74c3c"}
markers = {"Increase": "o", "Maintain": "s", "Reduce": "v"}

for _, row in df.iterrows():
    ax.scatter(row["perf_score"], row["risk_score"], 
               s=row["num_outlets"]*8, c=colors[row["recommendation"]], 
               alpha=0.7, edgecolors='black', linewidth=0.8, zorder=5)
    ax.annotate(row["Outlet Type"], (row["perf_score"], row["risk_score"]), 
                fontsize=9, fontweight='bold', ha='center', va='bottom',
                xytext=(0, 8), textcoords='offset points')

# Quadrant lines
ax.axhline(y=df["risk_score"].median(), color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=df["perf_score"].median(), color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel("Sales Performance Score (higher = better)", fontsize=12, fontweight='bold')
ax.set_ylabel("Risk / Complaint Score (higher = riskier)", fontsize=12, fontweight='bold')
ax.set_title("Coca-Cola Outlet Type Strategy: Performance vs Risk\n(Bubble size = number of outlets)", fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)

# Add quadrant labels
ax.text(0.02, 0.98, "Low Perf / High Risk\n→ REDUCE", transform=ax.transAxes, fontsize=10, 
        color='red', fontweight='bold', va='top', ha='left')
ax.text(0.98, 0.98, "High Perf / High Risk\n→ CAUTIOUS", transform=ax.transAxes, fontsize=10, 
        color='orange', fontweight='bold', va='top', ha='right')
ax.text(0.02, 0.02, "Low Perf / Low Risk\n→ MAINTAIN", transform=ax.transAxes, fontsize=10, 
        color='orange', fontweight='bold', va='bottom', ha='left')
ax.text(0.98, 0.02, "High Perf / Low Risk\n→ INCREASE", transform=ax.transAxes, fontsize=10, 
        color='green', fontweight='bold', va='bottom', ha='right')

plt.tight_layout()
plt.savefig("/work/performance_vs_risk.png", dpi=150)
plt.close()

# --- FIGURE 2: Composite Scores Bar Chart ---
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(df))
width = 0.25
bars1 = ax.bar(x - width, df["perf_score"], width, label='Performance Score', color='#3498db', alpha=0.85)
bars2 = ax.bar(x, df["risk_score"], width, label='Risk Score (inverted = lower better)', color='#e74c3c', alpha=0.85)
bars3 = ax.bar(x + width, df["health_score"], width, label='Relationship Health Score', color='#2ecc71', alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(df["Outlet Type"], rotation=30, ha='right', fontsize=9)
ax.set_ylabel("Composite Score (0-100)", fontweight='bold')
ax.set_title("Outlet Type Composite Scores: Performance, Risk & Relationship Health", fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("/work/composite_scores.png", dpi=150)
plt.close()

# --- FIGURE 3: Key Metrics Heatmap (normalized) ---
metrics_for_heatmap = ["avg_tar", "pos_target_ach", "avg_yoy", "avg_sales_value", 
                       "complaint_ratio", "quality_ratio", "appeals_per_outlet", 
                       "renewal_ratio", "renew_high_ratio", "avg_pass_rate"]

heat_df = df[["Outlet Type"] + metrics_for_heatmap].set_index("Outlet Type")
# Normalize each column to 0-1
heat_norm = (heat_df - heat_df.min()) / (heat_df.max() - heat_df.min())

fig, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(heat_norm, annot=True, fmt='.2f', cmap='RdYlGn', center=0.5,
            linewidths=0.8, ax=ax, cbar_kws={'label': 'Normalized Score (0=Low, 1=High)'})
ax.set_title("Normalized Key Metrics by Outlet Type\n(Green=Better, Red=Worse)", fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig("/work/metrics_heatmap.png", dpi=150)
plt.close()

print("All figures saved.")
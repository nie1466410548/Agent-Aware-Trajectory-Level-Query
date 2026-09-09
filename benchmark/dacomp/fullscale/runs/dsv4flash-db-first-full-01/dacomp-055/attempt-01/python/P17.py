import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv("/work/analysis_final.csv")

print("=== The IPS-Health Score Confound ===")
r, p = stats.pearsonr(df['ips'], df['health'])
print(f"  IPS vs Health: r={r:.3f}, p={p:.1e}")
r, p = stats.spearmanr(df['health'], df['roi'])
print(f"  Health vs ROI: r={r:.3f}, p={p:.2e}")
r, p = stats.spearmanr(df['health'], df['churn'])
print(f"  Health vs Churn: r={r:.3f}, p={p:.2e}")
r, p = stats.spearmanr(df['health'], df['par'])
print(f"  Health vs PAR: r={r:.3f}, p={p:.2e}")

print("\n=== What actually drives ROI? ===")
for col in ['team_size','par','sre','onboarding','total_sales_amount','acq','nps','digi_eng','churn','ttv','cpi','renew','expansion']:
    s = df[['roi', col]].dropna()
    if len(s) > 50:
        r, p = stats.spearmanr(s['roi'], s[col])
        print(f"  ROI vs {col:20s}: r={r:+.3f}, p={p:.2e}")

# Decision maker ROI correlation with IPS weighting
print("\n=== Decision Maker: implied priority vs realized ROI ===")
total_ips = df['ips'].sum()
for dm in ['C-Level','VP','Director','Manager','Individual Contributor']:
    grp = df[df['dm']==dm]
    print(f"  {dm:25s}: IPS_share={100*grp['ips'].sum()/total_ips:5.2f}%, avg_ROI={grp['roi'].mean():6.2f}")

print("\n=== Team size continuous effect on ROI ===")
r, p = stats.spearmanr(df['roi'], df['team_size'])
print(f"  ROI vs team_size: r={r:+.3f}, p={p:.2e}")
# partial: ROI vs team_size controlling for acq (informal)
print("\nDone.")
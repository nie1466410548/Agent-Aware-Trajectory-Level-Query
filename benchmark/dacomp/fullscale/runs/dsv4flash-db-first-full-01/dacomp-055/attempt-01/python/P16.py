import pandas as pd, numpy as np
df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1]
noncohort = df[df['is_target']==0]

# Investment allocation bias: IPS-weighted share vs actual value share
total_ips = df['ips'].sum()
total_acq = df['acq'].sum()
total_clv = df['clv'].sum()
total_sales = df['total_sales_amount'].sum()

print("=== Investment Allocation vs Actual Returns ===")
for name, grp in [('Target cohort', cohort), ('Non-cohort', noncohort), ('All', df)]:
    n = len(grp)
    ips_share = 100*grp['ips'].sum()/total_ips
    acq_share = 100*grp['acq'].sum()/total_acq
    clv_share = 100*grp['clv'].sum()/total_clv
    sales_share = 100*grp['total_sales_amount'].sum()/total_sales
    print(f"  {name:15s}: N={n:5d}, IPS_share={ips_share:5.1f}%, AcqCost_share={acq_share:5.1f}%, CLV_share={clv_share:5.1f}%, Sales_share={sales_share:5.1f}%")

# Bias by decision maker: implied vs actual
print("\n=== Decision Maker: IPS vs ROI ===")
for dm in ['C-Level','VP','Director','Manager','Individual Contributor']:
    grp = df[df['dm']==dm]
    ips_w = grp['ips'].sum()/total_ips
    roi_w = grp['roi'].mean()
    print(f"  {dm:25s}: N={len(grp):4d}, IPS_share={100*ips_w:5.2f}%, avg_ROI={roi_w:6.2f}")

# Size tier misalignment
print("\n=== Size Tier: ROI vs IPS priority ===")
for sz in ['Startup','Small','Medium','Large','Enterprise']:
    grp = df[df['company_size_tier']==sz]
    if len(grp)==0: continue
    print(f"  {sz:15s}: N={len(grp):4d}, avg_IPS={grp['ips'].mean():.3f}, avg_ROI={grp['roi'].mean():.2f}, ratio={grp['ips'].mean()/grp['roi'].mean():.4f}")

# The key finding: IPS is essentially a health score proxy, not a value metric
print("\n=== The IPS-Health Score Confound ===")
r, p = stats.pearsonr(df['ips'], df['health'])
print(f"  IPS vs Health: r={r:.3f}")
r, p = stats.pearsonr(df['health'], df['roi'])
print(f"  Health vs ROI: r={r:.3f}")
r, p = stats.pearsonr(df['health'], df['churn'])
print(f"  Health vs Churn: r={r:.3f}")
# health is NOT correlated with churn or ROI, but IS correlated with IPS
# So IPS is basically a renamed health score, not a value-based priority score

# What actually drives ROI?
print("\n=== What drives ROI? (correlation) ===")
for col in ['team_size','par','sre','onboarding','total_sales_amount','acq','nps','digi_eng','churn','ttv','cpi']:
    r, p = stats.spearmanr(df['roi'], df[col])
    print(f"  ROI vs {col:20s}: r={r:+.3f}, p={p:.2e}")

print("\nAll analysis complete.")
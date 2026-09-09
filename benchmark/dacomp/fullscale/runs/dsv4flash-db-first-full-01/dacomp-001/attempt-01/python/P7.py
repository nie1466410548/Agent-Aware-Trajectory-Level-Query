import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/final_allocation.csv')

# Per-rating profiles
print("=== PER-RATING PROFILES (all 123 credit-history firms) ===")
prof = df.groupby('rating').agg(
    n=('code','count'),
    defaults=('defaulted_flag','sum'),
    default_rate=('defaulted_flag','mean'),
    avg_revenue=('total_revenue','mean'),
    avg_margin=('margin','mean'),
    avg_cv=('cv','mean'),
    avg_top1_buyer=('top1_buyer','mean'),
    avg_top1_supplier=('top1_supplier','mean'),
    avg_risk=('risk_score','mean')
).round(4)
print(prof)

# Risk score discrimination: % of defaulted in each tier
print("\n=== RISK TIER vs DEFAULT ===")
tier_def = df.groupby('risk_tier').agg(n=('code','count'), defaults=('defaulted_flag','sum'))
tier_def['default_rate_%'] = tier_def['defaults']/tier_def['n']*100
print(tier_def.round(1))

# Example allocation table (top firms by credit)
print("\n=== TOP 10 FIRMS BY CREDIT LIMIT ===")
top = df.nlargest(10, 'credit_limit')[['code','rating','risk_tier','total_revenue','credit_limit','interest_rate']].copy()
top['credit_limit'] = top['credit_limit'].round(0)
top['total_revenue'] = top['total_revenue'].round(0)
top['interest_rate'] = (top['interest_rate']*100).round(2)
print(top.to_string())

# Bottom 5 D-rated example
print("\n=== SAMPLE D-RATED (defaulted) FIRMS ===")
d = df[df['rating']=='D'].sort_values('credit_limit', ascending=False).head(5)[['code','total_revenue','margin','cv','risk_score','credit_limit']].round(2)
print(d.to_string())

# Figure: risk factor comparison defaulted vs not
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
metrics = [('margin', 'Profit Margin'), ('cv', 'Revenue Volatility (CV)'), ('risk_score', 'Composite Risk Score')]
for ax, (col, title) in zip(axes, metrics):
    d0 = df[df['defaulted']=='No'][col]
    d1 = df[df['defaulted']=='Yes'][col]
    ax.boxplot([d0, d1], labels=['Non-defaulted', 'Defaulted'])
    ax.set_title(title)
    ax.set_ylabel('Value')
plt.tight_layout()
plt.savefig('/work/risk_factors.png', dpi=150)
plt.close()
print("\nSaved risk_factors.png")
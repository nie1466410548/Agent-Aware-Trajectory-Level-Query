import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('/work/final_allocation.csv')

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
metrics = [('margin', 'Profit Margin'), ('cv', 'Revenue Volatility (CV)'), ('risk_score', 'Composite Risk Score')]
for ax, (col, title) in zip(axes, metrics):
    d0 = df[df['defaulted']=='No'][col].values
    d1 = df[df['defaulted']=='Yes'][col].values
    bp = ax.boxplot([d0, d1])
    ax.set_xticklabels(['Non-defaulted', 'Defaulted'])
    ax.set_title(title)
    ax.set_ylabel('Value')
plt.tight_layout()
plt.savefig('/work/risk_factors.png', dpi=150)
plt.close()
print("Saved risk_factors.png")

# Final plan table for report - full by rating & tier (revised plan)
rev = pd.read_csv('/work/revised_plan.csv')
print("\n=== FINAL REVISED PLAN: by rating x tier ===")
final_tbl = rev.groupby(['rating','risk_tier']).agg(
    n=('code','count'),
    total_credit_wan=('credit_limit', lambda x: round(x.sum()/1e4, 1)),
    avg_credit_wan=('credit_limit', lambda x: round(x.mean()/1e4, 1)),
    avg_rate_pct=('interest_rate', lambda x: round(x.mean()*100, 2)),
    exp_income_wan=('expected_income', lambda x: round(x.sum()/1e4, 1))
)
print(final_tbl.to_string())
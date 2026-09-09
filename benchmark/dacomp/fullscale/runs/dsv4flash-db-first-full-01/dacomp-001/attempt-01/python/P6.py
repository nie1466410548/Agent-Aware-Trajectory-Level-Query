import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

res = db.query('SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"')
churn = db.frame(res)

print("Full churn rate table:")
print(churn.to_string())

# Compute expected return for each rate
for r in ['A','B','C']:
    col = f'Credit Rating {r} Customer Churn Rate'
    churn[f'exp_ret_{r}'] = churn['Annual Loan Interest Rate'] * (1 - churn[col])
    churn[f'retained_{r}'] = 1 - churn[col]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Churn rate vs interest rate
for r, c in [('A','green'),('B','blue'),('C','orange')]:
    col = f'Credit Rating {r} Customer Churn Rate'
    axes[0].plot(churn['Annual Loan Interest Rate']*100, churn[col]*100, 
                 marker='o', label=f'Rating {r}', color=c, linewidth=2)
axes[0].set_xlabel('Annual Loan Interest Rate (%)')
axes[0].set_ylabel('Customer Churn Rate (%)')
axes[0].set_title('Churn Rate vs Interest Rate')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Expected return vs interest rate
for r, c in [('A','green'),('B','blue'),('C','orange')]:
    axes[1].plot(churn['Annual Loan Interest Rate']*100, churn[f'exp_ret_{r}']*100, 
                 marker='o', label=f'Rating {r}', color=c, linewidth=2)
    # Mark optimal
    idx = churn[f'exp_ret_{r}'].idxmax()
    axes[1].plot(churn.loc[idx, 'Annual Loan Interest Rate']*100, churn.loc[idx, f'exp_ret_{r}']*100, 
                 marker='*', markersize=15, color=c)
axes[1].set_xlabel('Annual Loan Interest Rate (%)')
axes[1].set_ylabel('Expected Return Rate (%)')
axes[1].set_title('Expected Return Rate vs Interest Rate (* = optimal)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/rate_optimization.png', dpi=150)
plt.close()
print("Saved rate_optimization.png")

# Show optimal rates
print("\nOptimal rate selection:")
for r in ['A','B','C']:
    idx = churn[f'exp_ret_{r}'].idxmax()
    print(f"Rating {r}: rate={churn.loc[idx,'Annual Loan Interest Rate']:.4f} "
          f"({churn.loc[idx,'Annual Loan Interest Rate']*100:.2f}%), "
          f"churn={churn.loc[idx,f'Credit Rating {r} Customer Churn Rate']:.4f} "
          f"({churn.loc[idx,f'Credit Rating {r} Customer Churn Rate']*100:.2f}%), "
          f"expected return={churn.loc[idx,f'exp_ret_{r}']:.4f} "
          f"({churn.loc[idx,f'exp_ret_{r}']*100:.2f}%)")
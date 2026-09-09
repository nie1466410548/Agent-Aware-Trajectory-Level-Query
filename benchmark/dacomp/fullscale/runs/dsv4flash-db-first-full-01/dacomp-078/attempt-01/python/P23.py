import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set style
plt.rcParams.update({'figure.dpi': 110, 'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3})

trend = pd.read_csv('/work/monthly_trends.csv')
trend['month_num'] = trend['month'].str.slice(5,7).astype(int)

# Figure 1: Monthly value trends (minutes) for accounts with 5+ months
fig, ax = plt.subplots(figsize=(9, 5))
for acc, g in trend.groupby('account_id'):
    if len(g) >= 5:
        g = g.sort_values('month_num')
        lbl = acc.replace('ACC', 'Acct ')
        ax.plot(g['month_num'], g['month_minutes'], marker='o', ms=4, label=lbl)
ax.set_xlabel('Month (2024)')
ax.set_ylabel('Monthly usage minutes (all visitors)')
ax.set_title('Account monthly value trajectories (daily-metrics accounts, 5+ months)')
ax.legend(fontsize=8, ncol=2)
plt.tight_layout()
plt.savefig('figure1_monthly_value_trends.png')
plt.close()
print('figure1 saved')
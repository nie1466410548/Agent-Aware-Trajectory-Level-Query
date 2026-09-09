import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/project_data.csv')
df['comp_num'] = df['comp'].str.replace('%','').astype(float)

# In-progress: relation between deviation and completion %
df_ip = df[df['status']=='In Progress'].copy()
df_ip['remaining'] = 100 - df_ip['comp_num']
r, p = stats.spearmanr(df_ip['deviation'], df_ip['remaining'])
print(f"In-Progress projects: spearman(deviation, % remaining) = {r:.4f}, p={p:.6f}")
print(f"  n={len(df_ip)}")
# check if deviation is mostly explained by budget * remaining
df_ip['expected_remaining_cost'] = df_ip['budget'] * df_ip['remaining']/100
r2, p2 = stats.spearmanr(df_ip['deviation'], df_ip['expected_remaining_cost'])
print(f"  spearman(deviation, budget*remaining) = {r2:.4f}, p={p2:.6f}")

# Delayed projects - do they overspend?
df_del = df[df['status']=='Delayed']
print(f"\nDelayed projects: mean dev={df_del['deviation'].mean():.2f}, median={df_del['deviation'].median():.2f}")
print(f"  over budget: {(df_del['actual']>df_del['budget']).sum()}/{len(df_del)} ({(df_del['actual']>df_del['budget']).mean()*100:.1f}%)")
print(f"  by type: \n{df_del.groupby('Project Type')['deviation'].agg(['count','mean','median']).round(2).to_string()}")

# ---- Final figure: Grouped bar chart mean deviation by Type x Risk ----
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Grouped bar chart: mean deviation by Project Type and Risk Level
pivot = df.pivot_table(index='Project Type', columns='risk', values='deviation', aggfunc='mean').reindex(
    ['Software Development', 'Infrastructure', 'Marketing Promotion'])
pivot.plot(kind='bar', ax=axes[0], color=['#d62728', '#ff7f0e', '#2ca02c'])
axes[0].set_title('Mean Cost Deviation by Project Type & Risk Level (All Projects)', fontsize=13)
axes[0].set_ylabel('Mean Deviation (Budget - Actual)')
axes[0].tick_params(axis='x', rotation=15)
axes[0].legend(title='Risk Level')

# Grouped bar chart for completed only
dfc = df[df['status']=='Completed']
pivot_c = dfc.pivot_table(index='Project Type', columns='risk', values='deviation', aggfunc='mean').reindex(
    ['Software Development', 'Infrastructure', 'Marketing Promotion'])
pivot_c.plot(kind='bar', ax=axes[1], color=['#d62728', '#ff7f0e', '#2ca02c'])
axes[1].set_title('Mean Cost Deviation by Project Type & Risk Level (Completed)', fontsize=13)
axes[1].set_ylabel('Mean Deviation (Budget - Actual)')
axes[1].tick_params(axis='x', rotation=15)
axes[1].legend(title='Risk Level')

plt.tight_layout()
plt.savefig('/work/fig4_risk_interaction.png', dpi=100)
plt.close()
print("fig4 saved")

# ---- Another figure: deviation by status and type (stacked view) ----
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df, x='Project Type', y='deviation', hue='status', ci=None, ax=ax,
            palette='Set1')
ax.set_title('Mean Cost Deviation by Project Type & Project Status', fontsize=14)
ax.set_ylabel('Mean Deviation (Budget - Actual Cost)')
plt.tight_layout()
plt.savefig('/work/fig5_status_interaction.png', dpi=100)
plt.close()
print("fig5 saved")

# Distribution stats per type for report
print("\n--- Distribution statistics by Project Type (all) ---")
print(df.groupby('Project Type')['deviation'].agg(
    ['count','mean','std','median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75), 'min','max']).round(2).to_string())
print("\n--- Distribution statistics by Project Type (completed) ---")
print(dfc.groupby('Project Type')['deviation'].agg(
    ['count','mean','std','median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75), 'min','max']).round(2).to_string())
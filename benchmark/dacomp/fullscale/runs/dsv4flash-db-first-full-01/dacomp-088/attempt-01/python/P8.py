import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/final_analysis_v3.csv')

# 1. Full ranked list
fig, ax = plt.subplots(figsize=(14, 16))
colors = sns.color_palette("coolwarm", 50)
ax.barh(range(len(df)), df['investment_efficiency_score'].values, color=colors)
ax.set_yticks(range(len(df)))
ax.set_yticklabels([f"{r}. {s}" for r, s in zip(df['rank'], df['state'])])
ax.invert_yaxis()
ax.set_xlabel('Investment Efficiency Score')
ax.set_title('All 50 States Ranked by Investment Efficiency Score')
plt.tight_layout()
plt.savefig('/work/full_ranking.png', dpi=150)
plt.close()

# 2. Top 10 comparison panel
top10 = df.head(10)
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
metrics = [('CAC', 'CAC ($)', 'tab:red'),
           ('market_penetration', 'Market Penetration Rate', 'tab:blue'),
           ('sales_efficiency', 'Sales Efficiency', 'tab:green'),
           ('investment_return_score', 'Investment Return Score', 'tab:purple'),
           ('avg_revenue', 'Avg Annual Revenue ($M)', 'tab:orange'),
           ('competition_intensity_score', 'Competition Intensity', 'tab:gray')]
for ax, (col, label, color) in zip(axes.flat, metrics):
    vals = top10[col].fillna(0).values
    if col == 'avg_revenue':
        vals = vals / 1e6
    ax.bar(top10['state'], vals, color=color, alpha=0.75)
    ax.tick_params(axis='x', rotation=45)
    ax.set_title(label)
plt.suptitle('Top 10 States - Key Metrics Detail', fontsize=16)
plt.tight_layout()
plt.savefig('/work/top10_panel.png', dpi=150)
plt.close()

# 3. Competition vs Return scatter (all states)
fig, ax = plt.subplots(figsize=(12, 8))
sc = ax.scatter(df['competition_intensity_score'], df['investment_return_score'],
                c=df['investment_efficiency_score'], cmap='viridis', s=90, alpha=0.8)
for _, row in df.head(12).iterrows():
    ax.annotate(row['state'], (row['competition_intensity_score'], row['investment_return_score']), fontsize=9)
ax.set_xlabel('State Competition Intensity Score (model)')
ax.set_ylabel('Investment Return Prediction Score')
plt.colorbar(sc, label='Investment Efficiency Score')
plt.title('Competition Intensity vs Predicted Investment Return (50 states)')
plt.tight_layout()
plt.savefig('/work/comp_return_scatter.png', dpi=150)
plt.close()

# 4. CAC vs Penetration (states with data)
plot_df = df[df['CAC'].notna()]
fig, ax = plt.subplots(figsize=(12, 8))
sc = ax.scatter(plot_df['CAC'], plot_df['market_penetration'],
                c=plot_df['investment_efficiency_score'], cmap='plasma', s=90, alpha=0.8)
for _, row in plot_df.head(12).iterrows():
    ax.annotate(row['state'], (row['CAC'], row['market_penetration']), fontsize=9)
ax.set_xlabel('Customer Acquisition Cost ($)')
ax.set_ylabel('Market Penetration Rate')
plt.colorbar(sc, label='Investment Efficiency Score')
plt.title('CAC vs Market Penetration (states with customer data)')
plt.tight_layout()
plt.savefig('/work/cac_pen_scatter.png', dpi=150)
plt.close()

# Summary stats
print("Summary statistics:")
print(f"Total customers: {df['n_customers'].sum():.0f}, Total new customers: {df['n_new_customers'].sum():.0f}, Total reps: {df['n_reps'].sum():.0f}")
print(f"Median investment efficiency score: {df['investment_efficiency_score'].median():.2f}")
print(f"Top state: {df.iloc[0]['state']} ({df.iloc[0]['investment_efficiency_score']:.2f})")
print(f"Lowest state: {df.iloc[-1]['state']} ({df.iloc[-1]['investment_efficiency_score']:.2f})")

# Tier structure for recommendation
df['expansion_tier'] = df['rank'].apply(lambda r: 'Tier 1' if r<=10 else ('Tier 2' if r<=25 else 'Tier 3'))
tier_stats = df.groupby('expansion_tier').agg(
    avg_score=('investment_efficiency_score','mean'),
    avg_cac=('CAC','mean'),
    avg_return=('investment_return_score','mean'),
    avg_penetration=('market_penetration','mean')).round(2)
print("\nTier summary:")
print(tier_stats.to_string())

# Top industries overall (for context)
ind_overall = db.frame(db.query("""
    SELECT industry, COUNT(DISTINCT account_id) AS n
    FROM salesforce__account_daily_history WHERE type='Customer'
    GROUP BY industry ORDER BY n DESC LIMIT 8
"""))
print("\nTop customer industries overall:")
print(ind_overall.to_string())

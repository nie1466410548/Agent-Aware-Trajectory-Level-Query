import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# --- Pull all base data ---
rev = db.frame(db.query("""
    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
"""))

cust = db.frame(db.query("""
    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state
"""))

# New customers: accounts with won New Business opportunities (billing state)
new_cust = db.frame(db.query("""
    SELECT a.billing_state AS state, COUNT(DISTINCT a.account_id) AS n_new_customers
    FROM salesforce__account_daily_history a
    JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
    WHERE o.is_won = 1 AND o.type = 'New Business' AND a.billing_state IS NOT NULL
    GROUP BY a.billing_state
"""))

ind = db.frame(db.query("""
    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry
"""))

opp = db.frame(db.query("""
    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state
"""))

reps = db.frame(db.query("""
    SELECT billing_state AS state, COUNT(DISTINCT owner_id) AS n_reps
    FROM salesforce__account_daily_history
    WHERE billing_state IS NOT NULL
    GROUP BY billing_state
"""))

eco = db.frame(db.query("""
    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data
"""))

# --- Compute derived metrics ---
med = rev.groupby('state')['annual_revenue'].median().rename('median_revenue')
cust = cust.merge(med, on='state', how='left')
cust = cust.merge(new_cust, on='state', how='left')
cust['n_new_customers'] = cust['n_new_customers'].fillna(0)

ind['state_total'] = ind.groupby('state')['n_cust_industry'].transform('sum')
ind['share'] = ind['n_cust_industry'] / ind['state_total']
top3 = ind.sort_values(['state','share'], ascending=[True,False]).groupby('state').head(3)
conc = top3.groupby('state')['share'].sum().rename('industry_concentration')
cust = cust.merge(conc, on='state', how='left')

# Merge all
merged = eco.merge(cust, on='state', how='left')
merged = merged.merge(opp, on='state', how='left')
merged = merged.merge(reps, on='state', how='left')

# Fill NAs
fill_cols = ['n_customers','n_new_customers','avg_revenue','median_revenue','industry_concentration',
             'n_reps','n_opps','won_opps','avg_won_amount']
for c in fill_cols:
    merged[c] = merged[c].fillna(0)
merged['avg_won_prob'] = merged['avg_won_prob'].fillna(50)
merged['avg_won_cycle_days'] = merged['avg_won_cycle_days'].fillna(200)
merged['avg_probability'] = merged['avg_probability'].fillna(50)
merged['avg_cycle_days'] = merged['avg_cycle_days'].fillna(200)

# 1. CAC (using n_new_customers as "new customers")
merged['CAC'] = np.where(merged['n_new_customers'] > 0,
                          (merged['n_reps'] * 150000) / merged['n_new_customers'], 
                          np.nan)

# 3. Market Penetration
merged['market_penetration'] = merged['n_customers'] / (merged['population'] / 10000)

# 4. Sales Efficiency
merged['sales_efficiency'] = np.where(merged['avg_won_cycle_days'] > 0,
      (merged['avg_won_amount'] / merged['avg_won_cycle_days']) * (merged['avg_won_prob'] / 100), 0)

# Normalization helper
def minmax(s):
    mm = s.dropna()
    if len(mm) == 0: return s * 0.0
    mn, mx = mm.min(), mm.max()
    if mx == mn: return s * 0.0
    return (s - mn) / (mx - mn)

# 6. Competition Intensity Model
merged['comp_win_score'] = minmax(100 - merged['avg_probability'])
merged['comp_deal_score'] = minmax(merged['avg_won_amount'])
merged['comp_cycle_score'] = minmax(merged['avg_cycle_days'])
merged['competition_intensity_score'] = (merged['comp_win_score']*0.35 + 
                                          merged['comp_deal_score']*0.35 + 
                                          merged['comp_cycle_score']*0.30) * 100

# 7. Investment Return Prediction Algorithm
our_top = ['Technology', 'Manufacturing', 'Financial Services', 'Energy', 'Healthcare']
merged['industry_alignment'] = merged['primary_industry'].apply(lambda p: 1.0 if p in our_top else 0.5)
merged['inv_gdp_score'] = minmax(merged['gdp_per_capita'])
merged['inv_maturity_score'] = minmax(merged['market_maturity_score'])
merged['inv_biz_score'] = minmax(merged['business_friendly_index'])
merged['inv_comp_score'] = minmax(merged['competition_intensity'])
merged['investment_return_score'] = (merged['inv_gdp_score']*0.25 + merged['inv_maturity_score']*0.15 +
                                     merged['inv_biz_score']*0.20 + merged['industry_alignment']*0.15 +
                                     (1 - merged['inv_comp_score'])*0.25) * 100

# 8. Investment Efficiency Score (composite)
merged['n_CAC'] = 1 - minmax(merged['CAC'].fillna(merged['CAC'].max()*1.5))
merged['n_avg_rev'] = minmax(merged['avg_revenue'])
merged['n_med_rev'] = minmax(merged['median_revenue'])
merged['n_penetration'] = minmax(merged['market_penetration'])
merged['n_eff'] = minmax(merged['sales_efficiency'])
merged['n_conc'] = minmax(merged['industry_concentration'])
merged['n_comp'] = minmax(merged['competition_intensity_score'])
merged['n_return'] = minmax(merged['investment_return_score'])

merged['investment_efficiency_score'] = (
    merged['n_CAC']*0.15 + merged['n_avg_rev']*0.10 + merged['n_med_rev']*0.10 +
    merged['n_penetration']*0.15 + merged['n_eff']*0.15 + merged['n_conc']*0.05 +
    merged['n_comp']*0.10 + merged['n_return']*0.20) * 100

merged = merged.sort_values('investment_efficiency_score', ascending=False)
merged['rank'] = range(1, len(merged)+1)
merged.to_csv('/work/final_analysis.csv', index=False)

# --- Visualizations ---
plt.rcParams['figure.figsize'] = (14, 8)

# 1. Top 20 states by Investment Efficiency Score
top20 = merged.head(20)
fig, ax = plt.subplots(figsize=(14, 8))
colors = sns.color_palette("viridis", 20)
bars = ax.barh(range(len(top20)), top20['investment_efficiency_score'].values, color=colors)
ax.set_yticks(range(len(top20)))
ax.set_yticklabels(top20['state'].values)
ax.invert_yaxis()
ax.set_xlabel('Investment Efficiency Score')
ax.set_title('Top 20 States by Investment Efficiency Score')
for i, v in enumerate(top20['investment_efficiency_score'].values):
    ax.text(v + 0.5, i, f'{v:.1f}', va='center')
plt.tight_layout()
plt.savefig('/work/top20_scores.png', dpi=150)
plt.close()

# 2. Key metrics comparison for top 10
top10 = merged.head(10)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
metrics = [('CAC', 'CAC ($)', 'tab:red'), 
           ('market_penetration', 'Market Penetration', 'tab:blue'),
           ('sales_efficiency', 'Sales Efficiency', 'tab:green'),
           ('investment_return_score', 'Investment Return Score', 'tab:purple')]
for ax, (col, label, color) in zip(axes.flat, metrics):
    vals = top10[col].fillna(0).values
    ax.bar(top10['state'], vals, color=color, alpha=0.7)
    ax.set_xticklabels(top10['state'], rotation=45, ha='right')
    ax.set_title(label)
    ax.ticklabel_format(style='plain', axis='y')
plt.suptitle('Top 10 States - Key Metrics', fontsize=16)
plt.tight_layout()
plt.savefig('/work/top10_metrics.png', dpi=150)
plt.close()

# 3. Competition Intensity vs Investment Return scatter
fig, ax = plt.subplots(figsize=(12, 8))
sc = ax.scatter(merged['competition_intensity_score'], merged['investment_return_score'], 
                c=merged['investment_efficiency_score'], cmap='viridis', s=100, alpha=0.7)
for i, row in merged.head(15).iterrows():
    ax.annotate(row['state'], (row['competition_intensity_score'], row['investment_return_score']), fontsize=8)
ax.set_xlabel('Competition Intensity Score')
ax.set_ylabel('Investment Return Score')
plt.colorbar(sc, label='Investment Efficiency Score')
plt.title('Competition Intensity vs Investment Return by State')
plt.tight_layout()
plt.savefig('/work/comp_vs_return.png', dpi=150)
plt.close()

# 4. CAC vs Market Penetration
fig, ax = plt.subplots(figsize=(12, 8))
merged_plot = merged[merged['CAC'].notna() & (merged['n_customers']>0)]
sc = ax.scatter(merged_plot['CAC'], merged_plot['market_penetration'], 
                c=merged_plot['investment_efficiency_score'], cmap='plasma', s=100, alpha=0.7)
for i, row in merged_plot.head(15).iterrows():
    ax.annotate(row['state'], (row['CAC'], row['market_penetration']), fontsize=8)
ax.set_xlabel('CAC ($)')
ax.set_ylabel('Market Penetration Rate')
plt.colorbar(sc, label='Investment Efficiency Score')
plt.title('CAC vs Market Penetration by State')
plt.tight_layout()
plt.savefig('/work/cac_vs_penetration.png', dpi=150)
plt.close()

# Print summary tables
cols_display = ['rank','state','investment_efficiency_score','CAC','n_customers','n_new_customers','n_reps',
                'avg_revenue','median_revenue','market_penetration','sales_efficiency',
                'industry_concentration','competition_intensity_score','investment_return_score']
print("=== FINAL RANKING (Top 25) ===")
print(merged[cols_display].head(25).round(2).to_string())
print("\n=== FINAL RANKING (25-50) ===")
print(merged[cols_display].tail(25).round(2).to_string())

print("\n\n=== 3-YEAR EXPANSION TIERS ===")
# Tier 1: High Priority (top 10)
# Tier 2: Moderate Priority (11-25)
# Tier 3: Monitor (26-50)
merged['expansion_tier'] = merged['rank'].apply(
    lambda r: 'Tier 1: High Priority' if r <= 10 
    else ('Tier 2: Moderate Priority' if r <= 25 else 'Tier 3: Monitor/Develop'))
for tier in ['Tier 1: High Priority', 'Tier 2: Moderate Priority', 'Tier 3: Monitor/Develop']:
    subset = merged[merged['expansion_tier'] == tier]
    print(f"\n{tier}:")
    print(subset[['rank','state','investment_efficiency_score']].to_string(index=False))
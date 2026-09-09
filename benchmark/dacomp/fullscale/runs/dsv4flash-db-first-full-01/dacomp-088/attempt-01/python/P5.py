import pandas as pd, numpy as np

# ---- Pull data ----
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

# Reps per state: count distinct owners who have accounts in each state
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

# ---- Median revenue ----
med = rev.groupby('state')['annual_revenue'].median().rename('median_revenue')
cust = cust.merge(med, on='state', how='left')

# ---- Industry concentration ----
ind['state_total'] = ind.groupby('state')['n_cust_industry'].transform('sum')
ind['share'] = ind['n_cust_industry'] / ind['state_total']
top3 = ind.sort_values(['state','share'], ascending=[True,False]).groupby('state').head(3)
conc = top3.groupby('state')['share'].sum().rename('industry_concentration')
cust = cust.merge(conc, on='state', how='left')

# ---- Merge all (start with eco for all 50 states) ----
merged = eco.merge(cust, on='state', how='left')
merged = merged.merge(opp, on='state', how='left')
merged = merged.merge(reps, on='state', how='left')

# Fill NAs
merged['n_customers'] = merged['n_customers'].fillna(0)
merged['n_reps'] = merged['n_reps'].fillna(0)
merged['avg_revenue'] = merged['avg_revenue'].fillna(0)
merged['median_revenue'] = merged['median_revenue'].fillna(0)
merged['industry_concentration'] = merged['industry_concentration'].fillna(0)
merged['n_opps'] = merged['n_opps'].fillna(0)
merged['won_opps'] = merged['won_opps'].fillna(0)
merged['avg_won_amount'] = merged['avg_won_amount'].fillna(0)
merged['avg_won_prob'] = merged['avg_won_prob'].fillna(50)
merged['avg_won_cycle_days'] = merged['avg_won_cycle_days'].fillna(200)
merged['avg_probability'] = merged['avg_probability'].fillna(50)
merged['avg_cycle_days'] = merged['avg_cycle_days'].fillna(200)

# 1. CAC = (n_reps * 150000) / n_customers
merged['CAC'] = np.where(merged['n_customers'] > 0, 
                         (merged['n_reps'] * 150000) / merged['n_customers'], 
                         np.nan)

# 3. Market Penetration Rate
merged['market_penetration'] = merged['n_customers'] / (merged['population'] / 10000)

# 4. Sales Efficiency
merged['sales_efficiency'] = np.where(merged['avg_won_cycle_days'] > 0,
                                      (merged['avg_won_amount'] / merged['avg_won_cycle_days']) * (merged['avg_won_prob'] / 100),
                                      0)

# 6. Competition Intensity Model
def minmax(s):
    mm = s.dropna()
    if len(mm) == 0: return s
    mn, mx = mm.min(), mm.max()
    if mx == mn: return s * 0
    return (s - mn) / (mx - mn)

merged['comp_win_score'] = minmax(100 - merged['avg_probability'])
merged['comp_deal_score'] = minmax(merged['avg_won_amount'])
merged['comp_cycle_score'] = minmax(merged['avg_cycle_days'])
merged['competition_intensity_score'] = (merged['comp_win_score']*0.35 + merged['comp_deal_score']*0.35 + merged['comp_cycle_score']*0.30) * 100

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

# 8. Investment Efficiency Score
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
merged.to_csv('/work/full_state_analysis_v2.csv', index=False)

cols = ['rank','state','investment_efficiency_score','CAC','n_customers','n_reps','avg_revenue','median_revenue',
        'market_penetration','sales_efficiency','industry_concentration',
        'competition_intensity_score','investment_return_score']
print("Top 20 states:")
print(merged[cols].head(20).round(2).to_string())
print("\n\nBottom 10 states:")
print(merged[cols].tail(10).round(2).to_string())
print("\n\nAll states with their detailed metrics:")
print(merged[['rank','state','investment_efficiency_score']].to_string())
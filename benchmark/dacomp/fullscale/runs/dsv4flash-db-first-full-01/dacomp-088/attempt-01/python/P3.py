import pandas as pd, numpy as np

# ---- Pull data from database ----
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

reps = db.frame(db.query("""
    SELECT primary_state AS state, COUNT(*) AS n_reps
    FROM (
      SELECT owner_id, billing_state AS primary_state
      FROM (
        SELECT owner_id, billing_state, COUNT(*) AS cnt,
               ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
        FROM salesforce__account_daily_history
        WHERE billing_state IS NOT NULL
        GROUP BY owner_id, billing_state
      ) t
      WHERE rn = 1
    ) r
    GROUP BY primary_state
"""))

eco = db.frame(db.query("""
    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data
"""))

# ---- Median revenue per state ----
med = rev.groupby('state')['annual_revenue'].median().rename('median_revenue')
cust = cust.merge(med, on='state', how='left')

# ---- Industry concentration (top-3 industries share) ----
ind['state_total'] = ind.groupby('state')['n_cust_industry'].transform('sum')
ind['share'] = ind['n_cust_industry'] / ind['state_total']
top3 = ind.sort_values(['state','share'], ascending=[True,False]).groupby('state').head(3)
conc = top3.groupby('state')['share'].sum().rename('industry_concentration')
cust = cust.merge(conc, on='state', how='left')

# ---- Merge everything ----
merged = cust.merge(opp, on='state', how='left').merge(reps, on='state', how='left').merge(eco, on='state', how='left')
merged['n_reps'] = merged['n_reps'].fillna(0)
merged['n_opps'] = merged['n_opps'].fillna(0)
merged['won_opps'] = merged['won_opps'].fillna(0)
merged['avg_won_amount'] = merged['avg_won_amount'].fillna(0)
merged['avg_won_prob'] = merged['avg_won_prob'].fillna(50)
merged['avg_won_cycle_days'] = merged['avg_won_cycle_days'].fillna(200)
merged['avg_probability'] = merged['avg_probability'].fillna(50)
merged['avg_cycle_days'] = merged['avg_cycle_days'].fillna(200)

# 1. CAC
merged['CAC'] = (merged['n_reps'] * 150000) / merged['n_customers'].replace(0, np.nan)

# 3. Market Penetration Rate = n_customers / (population / 10000)
merged['market_penetration'] = merged['n_customers'] / (merged['population'] / 10000)

# 4. Sales Efficiency = avg_won_amount / avg_won_cycle_days * (avg_won_prob/100)
merged['sales_efficiency'] = (merged['avg_won_amount'] / merged['avg_won_cycle_days'].replace(0, np.nan)) * (merged['avg_won_prob'] / 100)

# 6. Competition Intensity Model: components = inverse win probability, deal size, sales cycle
comp_df = merged[['avg_probability', 'avg_won_amount', 'avg_cycle_days']].fillna(merged[['avg_probability', 'avg_won_amount', 'avg_cycle_days']].median())
inv_win = 100 - comp_df['avg_probability']
def minmax(s):
    return (s - s.min()) / (s.max() - s.min())
merged['comp_win_score'] = minmax(inv_win)
merged['comp_deal_score'] = minmax(comp_df['avg_won_amount'])
merged['comp_cycle_score'] = minmax(comp_df['avg_cycle_days'])
merged['competition_intensity_score'] = (merged['comp_win_score']*0.35 + merged['comp_deal_score']*0.35 + merged['comp_cycle_score']*0.30) * 100

# 7. Investment Return Prediction Algorithm
merged['population_density_rel'] = merged['population'] / merged['population'].mean()
our_top_industries = ['Technology', 'Manufacturing', 'Financial Services', 'Energy', 'Healthcare']
merged['industry_alignment'] = merged['primary_industry'].apply(lambda p: 1.0 if p in our_top_industries else 0.5)
merged['inv_gdp_score'] = minmax(merged['gdp_per_capita'])
merged['inv_maturity_score'] = minmax(merged['market_maturity_score'])
merged['inv_biz_score'] = minmax(merged['business_friendly_index'])
merged['inv_comp_score'] = minmax(merged['competition_intensity'])  # state's own competition intensity data
merged['investment_return_score'] = (merged['inv_gdp_score']*0.25 + merged['inv_maturity_score']*0.15 +
                                     merged['inv_biz_score']*0.20 + merged['industry_alignment']*0.15 +
                                     (1 - merged['inv_comp_score'])*0.25) * 100

# 8. Investment Efficiency Score (composite of all)
def norm(s):
    return (s - s.min()) / (s.max() - s.min())
merged['n_CAC'] = 1 - norm(merged['CAC'].fillna(merged['CAC'].max()))
merged['n_avg_rev'] = norm(merged['avg_revenue'])
merged['n_med_rev'] = norm(merged['median_revenue'])
merged['n_penetration'] = norm(merged['market_penetration'])
merged['n_eff'] = norm(merged['sales_efficiency'])
merged['n_conc'] = norm(merged['industry_concentration'])
merged['n_comp'] = norm(merged['competition_intensity_score'])
merged['n_return'] = norm(merged['investment_return_score'])

merged['investment_efficiency_score'] = (
    merged['n_CAC']*0.15 + merged['n_avg_rev']*0.10 + merged['n_med_rev']*0.10 +
    merged['n_penetration']*0.15 + merged['n_eff']*0.15 + merged['n_conc']*0.05 +
    merged['n_comp']*0.10 + merged['n_return']*0.20) * 100

merged = merged.sort_values('investment_efficiency_score', ascending=False)
merged['rank'] = range(1, len(merged)+1)
merged.to_csv('/work/full_state_analysis.csv', index=False)

cols = ['state','rank','investment_efficiency_score','CAC','avg_revenue','median_revenue',
        'market_penetration','sales_efficiency','industry_concentration',
        'competition_intensity_score','investment_return_score']
print(merged[cols].head(15).round(2).to_string())
print("\nBottom 10:")
print(merged[cols].tail(10).round(2).to_string())

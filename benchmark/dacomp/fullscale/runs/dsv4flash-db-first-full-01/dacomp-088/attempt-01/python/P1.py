import pandas as pd, numpy as np

# Customer revenue rows per state
rev = db.frame(db.query("""
    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
"""))

# State-level customer aggregates
cust = db.frame(db.query("""
    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state
"""))

# Industry concentration per state
ind = db.frame(db.query("""
    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry
"""))

# Opportunity stats per state
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

# Reps per state
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

# Economic data
eco = db.frame(db.query("""
    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data
"""))

print("rev", rev.shape, "cust", cust.shape, "ind", ind.shape, "opp", opp.shape, "reps", reps.shape, "eco", eco.shape)

# Median revenue per state
med = rev.groupby('state')['annual_revenue'].median().rename('median_revenue')
cust = cust.merge(med, on='state', how='left')

# Industry concentration: share of top-3 industries within state (by customer count)
ind['state_total'] = ind.groupby('state')['n_cust_industry'].transform('sum')
ind['share'] = ind['n_cust_industry'] / ind['state_total']
top3 = ind.sort_values(['state','share'], ascending=[True,False]).groupby('state').head(3)
conc = top3.groupby('state')['share'].sum().rename('industry_concentration')
cust = cust.merge(conc, on='state', how='left')

print(cust.head(10))
print(cust.shape)
cust.to_csv('/work/state_customer_metrics.csv', index=False)

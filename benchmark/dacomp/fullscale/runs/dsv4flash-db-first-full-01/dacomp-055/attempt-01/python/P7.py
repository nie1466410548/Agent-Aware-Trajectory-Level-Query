import pandas as pd, numpy as np

# Fetch from value_analysis table in chunks
chunks = []
for offset in range(0, 5001, 2000):
    sql = f"""
    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET {offset}
    """
    res = db.query(sql)
    rows = db.rows(res)
    chunks.append(pd.DataFrame(rows))
    print(f"offset {offset}: got {len(rows)} rows")

df_v = pd.concat(chunks, ignore_index=True)
print(f"Total rows: {len(df_v)}")
print(f"Distinct emails: {df_v['primary_email'].nunique()}")
print(f"Distinct key triples: {df_v['marketo_lead_id'].astype(str).str.cat(df_v['stripe_customer_id'].astype(str).str.cat(df_v['zendesk_user_id'].astype(str))).nunique()}")
df_v.to_csv("/work/value_analysis_full.csv", index=False)
print("Saved to /work/value_analysis_full.csv")
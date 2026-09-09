
import pandas as pd, numpy as np

# Reload df (it persists in the worker? safer to re-derive)
result = db.query("""
SELECT 
  account_id, count_associated_visitors, avg_nps_rating,
  count_active_visitors, count_page_viewing_visitors, count_feature_clicking_visitors,
  count_active_days, count_active_months, sum_minutes, sum_events,
  average_daily_minutes, average_daily_events, first_event_on, last_event_on,
  CAST(count_active_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS active_visitor_ratio,
  CAST(count_page_viewing_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS page_view_ratio,
  CAST(count_feature_clicking_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS feature_click_ratio,
  CAST(sum_minutes AS REAL) / NULLIF(count_active_days, 0) AS minutes_per_active_day,
  CAST(sum_events AS REAL) / NULLIF(count_active_days, 0) AS events_per_active_day
FROM pendo__account ORDER BY account_id
""")
df = db.frame(result)

# Outcome A: retained = last activity after mid-year (Jul 1 2024)
df['last_dt'] = pd.to_datetime(df['last_event_on'])
df['retained'] = (df['last_dt'] >= '2024-07-01').astype(int)
# Outcome B: retained at least 6 months (last activity >= Jul 1, given start ~Jan)
print('Retained after Jul 1:', df['retained'].sum(), '/', len(df))
print('Retention rate:', df['retained'].mean().round(3))

# Impute NPS (median) - NPS missing likely not missing-at-random, but fine for demo
df['avg_nps_rating'] = df['avg_nps_rating'].fillna(df['avg_nps_rating'].median())

# Save base df to /work
df.to_csv('/work/account_base.csv', index=False)
print('saved')

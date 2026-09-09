
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load person-level data
df = db.frame(db.query("""
SELECT person_id, days_span, active_days, active_months, months_span,
       paid_retained_month_count, paid_retention_rate_month,
       active_retention_rate_month, email_open_rate, count_received_email,
       count_opened_email, count_clicked_email, count_placed_order,
       sum_revenue_placed_order, count_viewed_product, has_7day_retention, has_30day_retention
FROM klaviyo__persons
"""))
print("Persons rows:", len(df))

# Derived speed/engagement metrics
df['density'] = df['active_days'] / df['days_span']
df['emails_per_month'] = df['count_received_email'] / df['active_months']
df['order_value'] = df['sum_revenue_placed_order'] / df['count_placed_order'].replace(0, np.nan)

# Correlation matrix between key metrics
cols = ['days_span','active_months','paid_retained_month_count','paid_retention_rate_month',
        'email_open_rate','count_received_email','count_clicked_email','count_placed_order',
        'sum_revenue_placed_order','density','emails_per_month']
cdf = df[cols].dropna()
corr = cdf.corr(method='pearson')

# Correlation with p-values for key relationships
def corr_p(x, y):
    x = df[x].values.astype(float); y = df[y].values.astype(float)
    mask = ~(np.isnan(x) | np.isnan(y))
    r, p = stats.pearsonr(x[mask], y[mask])
    return r, p

print("\nKey correlations (r, p):")
pairs = [
    ('days_span','count_placed_order'),('days_span','sum_revenue_placed_order'),
    ('days_span','paid_retention_rate_month'),('days_span','email_open_rate'),
    ('density','count_placed_order'),('density','paid_retention_rate_month'),
    ('email_open_rate','count_placed_order'),('email_open_rate','sum_revenue_placed_order'),
    ('count_received_email','email_open_rate'),('count_received_email','count_placed_order'),
    ('emails_per_month','count_placed_order'),('emails_per_month','email_open_rate'),
    ('active_months','count_placed_order'),('count_clicked_email','count_placed_order'),
]
for a,b in pairs:
    r,p = corr_p(a,b)
    print(f"  {a:28s} vs {b:28s}: r={r:+.3f}, p={p:.2e}")

print("\nCorrelation matrix:\n", corr.round(3).to_string())

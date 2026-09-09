import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# ====== Customer-level CV computation from Python (using archived data) ======
# I'll reconstruct from the database via db.query for the per-customer monthly gross profit
# Use db.query to fetch the necessary data

# First, get high/low vol segment assignment
sql_seg = """
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
)
SELECT customer_id, vol,
  CASE WHEN rn <= total * 0.25 THEN 'HighVol'
       WHEN rn > total * 0.75 THEN 'LowVol'
       ELSE 'MidVol' END AS vol_segment
FROM ordered
"""
seg_df = db.frame(db.query(sql_seg))

# Get monthly gross profit per customer over past 12 months
sql_monthly = """
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
)
SELECT customer_id, STRFTIME('%Y-%m', transaction_date) AS month, SUM(gross_profit) AS monthly_gp
FROM quickbooks__profitability_analysis
WHERE transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY customer_id, STRFTIME('%Y-%m', transaction_date)
"""
monthly_df = db.frame(db.query(sql_monthly))

# Merge and compute per-customer CV
merged = monthly_df.merge(seg_df[['customer_id', 'vol_segment']], on='customer_id', how='left')
merged = merged[merged['vol_segment'].isin(['HighVol', 'LowVol'])]

cv_by_cust = merged.groupby(['customer_id', 'vol_segment'])['monthly_gp'].agg(['mean', 'std', 'count']).reset_index()
cv_by_cust['cv'] = np.where(cv_by_cust['mean'] != 0, cv_by_cust['std'] / np.abs(cv_by_cust['mean']), np.nan)
cv_by_cust = cv_by_cust.dropna(subset=['cv'])

hv_cv = cv_by_cust[cv_by_cust['vol_segment'] == 'HighVol']['cv']
lv_cv = cv_by_cust[cv_by_cust['vol_segment'] == 'LowVol']['cv']

print("=== Customer-level CV of Monthly Gross Profit ===")
print(f"HighVol: n={len(hv_cv)}, mean CV={hv_cv.mean():.4f}, median={hv_cv.median():.4f}")
print(f"LowVol:  n={len(lv_cv)}, mean CV={lv_cv.mean():.4f}, median={lv_cv.median():.4f}")
t_stat, p_val = stats.mannwhitneyu(hv_cv, lv_cv, alternative='two-sided')
print(f"Mann-Whitney U: p={p_val:.4f}")

# ====== Revenue trend correlation: share of negative correlations ======
sql_trend = """
SELECT s.vol_segment, a.customer_id, a.revenue_trend_correlation
FROM (
  WITH cust_vol AS (
    SELECT customer_id, AVG(customer_margin_volatility) AS vol
    FROM quickbooks__profitability_analysis
    GROUP BY customer_id
  ),
  ordered AS (
    SELECT customer_id, vol,
      ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
      COUNT(*) OVER () AS total
    FROM cust_vol
  )
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
) s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
"""
trend_df = db.frame(db.query(sql_trend))
trend_df['negative_trend'] = trend_df['revenue_trend_correlation'] < 0
neg_share = trend_df.groupby('vol_segment')['negative_trend'].agg(['mean', 'count'])
print("\n=== Negative Revenue Trend Correlation Share ===")
print(neg_share)
print(f"Mean trend corr by segment: {trend_df.groupby('vol_segment')['revenue_trend_correlation'].mean()}")

# Chi-square test on negative trend share
table_neg = np.array([
    [trend_df[(trend_df.vol_segment=='HighVol') & (trend_df.negative_trend)].shape[0],
     trend_df[(trend_df.vol_segment=='HighVol') & (~trend_df.negative_trend)].shape[0]],
    [trend_df[(trend_df.vol_segment=='LowVol') & (trend_df.negative_trend)].shape[0],
     trend_df[(trend_df.vol_segment=='LowVol') & (~trend_df.negative_trend)].shape[0]],
])
chi2, p, dof, exp = stats.chi2_contingency(table_neg)
print(f"\nChi-sq negative trend HighVol vs LowVol: chi2={chi2:.3f}, p={p:.4f}")

# ====== Customer-level CV histogram ======
fig, ax = plt.subplots(figsize=(10, 6))
bins = np.linspace(0, max(hv_cv.max(), lv_cv.max()), 30)
ax.hist(hv_cv, bins=bins, alpha=0.6, label=f'HighVol (n={len(hv_cv)}, mean={hv_cv.mean():.2f})', color='#D32F2F', density=True)
ax.hist(lv_cv, bins=bins, alpha=0.6, label=f'LowVol (n={len(lv_cv)}, mean={lv_cv.mean():.2f})', color='#4CAF50', density=True)
ax.set_xlabel('Coefficient of Variation of Monthly Gross Profit')
ax.set_ylabel('Density')
ax.set_title('Profit Stability (CV of Monthly Gross Profit) Distribution by Volatility Segment')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig6_customer_cv_distribution.png', dpi=120, bbox_inches='tight')
plt.close()
print("\nFigure 6 saved: /work/fig6_customer_cv_distribution.png")
import pandas as pd, numpy as np
from scipy import stats

# Fetch data in chunks
all_rows = []
all_cols = None
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
    cols = res['executions'][0]['columns']
    rows = db.rows(res)
    if all_cols is None:
        all_cols = cols
    all_rows.extend(rows)

df_v = pd.DataFrame(all_rows, columns=all_cols)
print(f"Total rows: {len(df_v)}, columns: {list(df_v.columns)}")
print(f"Distinct emails: {df_v['primary_email'].nunique()}")

# Now fetch sales data per email
sales_sql = """
SELECT email, MAX(total_sales_amount) AS total_sales_amount
FROM customer360__customer
WHERE total_sales_amount IS NOT NULL AND email IS NOT NULL
GROUP BY email
"""
res2 = db.query(sales_sql)
cols2 = res2['executions'][0]['columns']
rows2 = db.rows(res2)
df_sales = pd.DataFrame(rows2, columns=cols2)
print(f"Sales data: {len(df_sales)} emails")

# Merge
df = df_v.merge(df_sales, left_on='primary_email', right_on='email', how='left')
print(f"Merged: {len(df)} rows")

# Drop exact duplicates
df = df.drop_duplicates()
print(f"After dedup: {len(df)} rows")

# Filter to complete cases
complete = df[['ips','par','sre','acq','clv','total_sales_amount']].notna().all(axis=1)
df = df[complete].copy()
print(f"Complete cases: {len(df)}")

# Compute composite score (min-max normalized)
min_sales, max_sales = df['total_sales_amount'].min(), df['total_sales_amount'].max()
min_par, max_par = df['par'].min(), df['par'].max()
min_sre, max_sre = df['sre'].min(), df['sre'].max()

df['nsales'] = (df['total_sales_amount'] - min_sales) / (max_sales - min_sales) if max_sales > min_sales else 0
df['nadopt'] = (df['par'] - min_par) / (max_par - min_par) if max_par > min_par else 0
df['nres'] = (df['sre'] - min_sre) / (max_sre - min_sre) if max_sre > min_sre else 0
df['composite'] = 0.4*df['nsales'] + 0.35*df['nadopt'] + 0.25*df['nres']
df['roi'] = df['clv'] / df['acq']

# Determine cohorts
n = len(df)
df['ips_rank_pct'] = df['ips'].rank(pct=True)
df['comp_rank_pct'] = df['composite'].rank(pct=True)
df['is_target'] = ((df['ips_rank_pct'] >= 0.7) & (df['comp_rank_pct'] <= 0.5)).astype(int)

print(f"\nTarget cohort size: {df['is_target'].sum()} out of {n}")
print(f"Top 30% IPS: {(df['ips_rank_pct'] >= 0.7).sum()}")
print(f"Bottom 50% composite: {(df['comp_rank_pct'] <= 0.5).sum()}")

# ===== CORRELATION ANALYSIS =====
print("\n" + "="*60)
print("CORRELATION: Onboarding Score vs Product Adoption Rate")
print("="*60)
sub = df.dropna(subset=['onboarding','par'])
print(f"N={len(sub)}")
r_p, p_p = stats.pearsonr(sub['onboarding'], sub['par'])
r_s, p_s = stats.spearmanr(sub['onboarding'], sub['par'])
print(f"All customers: Pearson r={r_p:.4f}, p={p_p:.2e}")
print(f"All customers: Spearman r={r_s:.4f}, p={p_s:.2e}")

# Cohort only
sub_c = df[df['is_target']==1].dropna(subset=['onboarding','par'])
r_pc, p_pc = stats.pearsonr(sub_c['onboarding'], sub_c['par'])
r_sc, p_sc = stats.spearmanr(sub_c['onboarding'], sub_c['par'])
print(f"Cohort only:    Pearson r={r_pc:.4f}, p={p_pc:.2e}, N={len(sub_c)}")
print(f"Cohort only:    Spearman r={r_sc:.4f}, p={p_sc:.2e}")

# Non-cohort
sub_nc = df[df['is_target']==0].dropna(subset=['onboarding','par'])
r_pnc, p_pnc = stats.pearsonr(sub_nc['onboarding'], sub_nc['par'])
r_snc, p_snc = stats.spearmanr(sub_nc['onboarding'], sub_nc['par'])
print(f"Non-cohort:     Pearson r={r_pnc:.4f}, p={p_pnc:.2e}, N={len(sub_nc)}")
print(f"Non-cohort:     Spearman r={r_snc:.4f}, p={p_snc:.2e}")

# ===== T-TESTS =====
print("\n" + "="*60)
print("COHORT vs NON-COHORT T-TESTS")
print("="*60)
metrics = ['onboarding','par','sre','roi','team_size','nps','digi_eng','health','churn','total_sales_amount','composite','ips']
for m in metrics:
    a = df.loc[df['is_target']==1, m].dropna()
    b = df.loc[df['is_target']==0, m].dropna()
    t, p = stats.ttest_ind(a, b, equal_var=False)
    print(f"{m:15s}  cohort_mean={a.mean():8.3f}  noncohort_mean={b.mean():8.3f}  t={t:7.2f}  p={p:.2e}")

# ===== DECISION MAKER LEVEL ANALYSIS =====
print("\n" + "="*60)
print("DECISION MAKER LEVEL DISTRIBUTION")
print("="*60)
dm_cross = pd.crosstab(df['dm'], df['is_target'], margins=True)
print(dm_cross)

# ===== TEAM SIZE ANALYSIS =====
print("\n" + "="*60)
print("TEAM SIZE BUCKET ANALYSIS")
print("="*60)
df['team_bucket'] = pd.cut(df['team_size'], bins=[0,2,5,10,20,999], labels=['1-2','3-5','6-10','11-20','20+'])
team_agg = df.groupby('team_bucket').agg(
    total=('is_target','count'),
    cohort=('is_target','sum'),
    cohort_pct=('is_target', lambda x: 100*x.mean()),
    avg_roi_cohort=('roi', lambda x: x[df.loc[x.index,'is_target']==1].mean()),
    avg_roi_noncohort=('roi', lambda x: x[df.loc[x.index,'is_target']==0].mean())
).reset_index()
print(team_agg)

# ===== INDUSTRY VERTICAL ANALYSIS =====
print("\n" + "="*60)
print("INDUSTRY VERTICAL ANALYSIS")
print("="*60)
ind_agg = df.groupby('industry_vertical').agg(
    total=('is_target','count'),
    cohort=('is_target','sum'),
    cohort_pct=('is_target', lambda x: 100*x.mean()),
    avg_roi=('roi', 'mean'),
    avg_roi_cohort=('roi', lambda x: x[df.loc[x.index,'is_target']==1].mean()),
    avg_par_cohort=('par', lambda x: x[df.loc[x.index,'is_target']==1].mean())
).reset_index().sort_values('cohort', ascending=False)
print(ind_agg.to_string())

# ===== COMPANY SIZE TIER =====
print("\n" + "="*60)
print("COMPANY SIZE TIER ANALYSIS")
print("="*60)
size_agg = df.groupby('company_size_tier').agg(
    total=('is_target','count'),
    cohort=('is_target','sum'),
    cohort_pct=('is_target', lambda x: 100*x.mean()),
    avg_roi_cohort=('roi', lambda x: x[df.loc[x.index,'is_target']==1].mean()),
    avg_roi_noncohort=('roi', lambda x: x[df.loc[x.index,'is_target']==0].mean()),
    avg_onb_cohort=('onboarding', lambda x: x[df.loc[x.index,'is_target']==1].mean()),
    avg_onb_noncohort=('onboarding', lambda x: x[df.loc[x.index,'is_target']==0].mean())
).reset_index().sort_values('cohort', ascending=False)
print(size_agg.to_string())

# ===== INVESTMENT BIAS ANALYSIS =====
print("\n" + "="*60)
print("INVESTMENT BIAS ANALYSIS")
print("="*60)
# Compare IPS vs actual ROI
df['ips_under_roi'] = (df['roi'] < df['ips']).astype(int)
print(f"Customers where ROI < IPS: {df['ips_under_roi'].mean()*100:.1f}%")

# Concentration by industry
print("\nCohort concentration (% of industry) by industry:")
for ind in sorted(df['industry_vertical'].dropna().unique()):
    sub = df[df['industry_vertical']==ind]
    pct = 100*sub['is_target'].mean()
    print(f"  {ind:20s}: {pct:5.1f}%  (n={len(sub)}, cohort={sub['is_target'].sum()})")

# Bias in decision_maker_level scoring
print("\nIPS overestimation by decision_maker_level:")
for dm in sorted(df['dm'].dropna().unique()):
    sub = df[df['dm']==dm]
    print(f"  {dm:20s}: avg_IPS={sub['ips'].mean():.3f}, avg_ROI={sub['roi'].mean():.3f}, ratio={sub['ips'].mean()/sub['roi'].mean():.4f}")

print("\nAnalysis complete. Saving dataset...")
df.to_csv("/work/analysis_complete.csv", index=False)
print("Saved to /work/analysis_complete.csv")
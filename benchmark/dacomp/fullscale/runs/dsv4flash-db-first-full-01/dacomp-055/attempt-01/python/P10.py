import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load full data
df = pd.read_csv("/work/analysis_complete.csv")

# Dedupe on primary analysis columns (same as SQL DISTINCT on those columns)
dedup_cols = ['primary_email','ips','par','sre','acq','clv','total_sales_amount',
              'lifecycle_stage','industry_vertical','company_size_tier','onboarding','team_size','dm']
df = df.drop_duplicates(subset=dedup_cols).copy()
print(f"Deduped rows: {len(df)}")

# Recompute composite & ranks to match SQL exactly
min_sales, max_sales = df['total_sales_amount'].min(), df['total_sales_amount'].max()
min_par, max_par = df['par'].min(), df['par'].max()
min_sre, max_sre = df['sre'].min(), df['sre'].max()
df['nsales'] = (df['total_sales_amount'] - min_sales) / (max_sales - min_sales)
df['nadopt'] = (df['par'] - min_par) / (max_par - min_par)
df['nres'] = (df['sre'] - min_sre) / (max_sre - min_sre)
df['composite'] = 0.4*df['nsales'] + 0.35*df['nadopt'] + 0.25*df['nres']
df['roi'] = df['clv'] / df['acq']

n = len(df)
df['ips_rn_pct'] = df['ips'].rank(method='first', ascending=True) / n
df['comp_rn_pct'] = df['composite'].rank(method='first', ascending=True) / n
df['is_target'] = ((df['ips_rn_pct'] >= 0.7) & (df['comp_rn_pct'] <= 0.5)).astype(int)
print(f"Total: {n}, Target cohort: {df['is_target'].sum()}")

# ============ VISUALIZATION 1: Cohort by lifecycle stage ============
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
lc = df.groupby('lifecycle_stage').agg(
    total=('is_target','count'),
    cohort=('is_target','sum'),
    avg_roi=('roi', lambda x: x[df.loc[x.index,'is_target']==1].mean())
).reindex(['Activation','Growth','Maturity','Retention','Dormant'])

axes[0].bar(lc.index, lc['cohort'], color='#c44e52')
for i,(idx,row) in enumerate(lc.iterrows()):
    axes[0].text(i, row['cohort']+3, f"{row['cohort']}", ha='center')
axes[0].set_title('Target Cohort Size by Lifecycle Stage')
axes[0].set_ylabel('Customers')

axes[1].bar(lc.index, lc['avg_roi'], color='#4c72b0')
for i,(idx,row) in enumerate(lc.iterrows()):
    axes[1].text(i, row['avg_roi']+0.3, f"{row['avg_roi']:.1f}", ha='center')
axes[1].set_title('Avg ROI (CLV/Acquisition Cost) by Lifecycle Stage')
axes[1].set_ylabel('ROI ratio')
plt.tight_layout()
plt.savefig("/work/fig_lifecycle.png", dpi=110)
plt.close()
print("Saved fig_lifecycle.png")

# ============ VISUALIZATION 2: Industry x Size heatmap ============
pivot = df.pivot_table(index='industry_vertical', columns='company_size_tier',
                       values='is_target', aggfunc='mean')
fig, ax = plt.subplots(figsize=(11, 6))
sns.heatmap(pivot*100, annot=True, fmt='.1f', cmap='Reds', cbar_kws={'label':'% of customers in target cohort'}, ax=ax)
ax.set_title('Target Cohort Share (%) by Industry Vertical and Company Size Tier')
plt.tight_layout()
plt.savefig("/work/fig_industry_size.png", dpi=110)
plt.close()
print("Saved fig_industry_size.png")

# ============ VISUALIZATION 3: Onboarding vs PAR scatter ============
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
sns.scatterplot(data=df, x='onboarding', y='par', hue='is_target', alpha=0.5, s=15, ax=ax)
# Regression lines
for t, color, lbl in [(0,'#c44e52','non-cohort'),(1,'#4c72b0','target cohort')]:
    sub = df[df['is_target']==t]
    sns.regplot(data=sub, x='onboarding', y='par', scatter=False, color=color, ax=ax, label=lbl)
ax.set_title(f'Onboarding Score vs Product Adoption Rate\nAll (r={stats.pearsonr(df["onboarding"], df["par"])[0]:.3f})')
ax.legend()
ax2 = axes[1]
sub_c = df[df['is_target']==1]
sns.scatterplot(data=sub_c, x='onboarding', y='par', alpha=0.6, s=18, color='#4c72b0', ax=ax2)
sns.regplot(data=sub_c, x='onboarding', y='par', scatter=False, color='#c44e52', ax=ax2)
r_c, p_c = stats.pearsonr(sub_c['onboarding'], sub_c['par'])
ax2.set_title(f'Target Cohort Only\nr={r_c:.3f}, p={p_c:.1e}')
plt.tight_layout()
plt.savefig("/work/fig_onboarding_corr.png", dpi=110)
plt.close()
print("Saved fig_onboarding_corr.png")

# ============ VISUALIZATION 4: Team size & decision maker ============
df['team_bucket'] = pd.cut(df['team_size'], bins=[0,2,5,10,20,999], labels=['1-2','3-5','6-10','11-20','20+'])
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
tb = df.groupby('team_bucket').agg(cohort_pct=('is_target','mean'), avg_roi=('roi','mean'))
axes[0].bar(tb.index.astype(str), 100*tb['cohort_pct'], color='#c44e52', alpha=0.8, label='% in target cohort')
axes[0].set_ylabel('% in target cohort', color='#c44e52')
ax2 = axes[0].twinx()
ax2.plot(tb.index.astype(str), tb['avg_roi'], color='#4c72b0', marker='o', label='Avg ROI (all)')
ax2.set_ylabel('Avg ROI ratio', color='#4c72b0')
axes[0].set_title('Team Size: Cohort Share vs Avg ROI')
axes[0].set_xlabel('Team size bucket')

dm_agg = df.groupby('dm').agg(cohort_pct=('is_target','mean'), avg_roi_cohort=('roi', lambda x: x[df.loc[x.index,'is_target']==1].mean()), avg_roi=('roi','mean'))
order = ['C-Level','VP','Director','Manager','Individual Contributor']
dm_agg = dm_agg.reindex(order)
axes[1].bar(dm_agg.index, 100*dm_agg['cohort_pct'], color='#55a868')
axes[1].set_ylabel('% in target cohort')
axes[1].set_title('Decision Maker Level: % in Target Cohort')
axes[1].tick_params(axis='x', rotation=15)
plt.tight_layout()
plt.savefig("/work/fig_team_dm.png", dpi=110)
plt.close()
print("Saved fig_team_dm.png")

# ============ EXTRA STATS for report ============
print("\n--- ROI by lifecycle (cohort) ---")
print(lc[['cohort','avg_roi']])

print("\n--- Correlation of onboarding vs PAR by decision maker ---")
for dm in order:
    sub = df[df['dm']==dm].dropna(subset=['onboarding','par'])
    if len(sub) > 10:
        r, p = stats.pearsonr(sub['onboarding'], sub['par'])
        print(f"  {dm:20s}: r={r:.3f}, p={p:.2e}, N={len(sub)}")

print("\n--- IPS thresholds ---")
print(f"70th pct IPS threshold: {df['ips'].quantile(0.7):.2f}")
print(f"50th pct composite threshold: {df['composite'].quantile(0.5):.4f}")

print("\n--- Onboarding by lifecycle stage (cohort vs non) ---")
onb_lc = df.groupby('lifecycle_stage').apply(lambda g: pd.Series({
    'cohort_avg_onb': g.loc[g['is_target']==1,'onboarding'].mean(),
    'noncohort_avg_onb': g.loc[g['is_target']==0,'onboarding'].mean(),
    'cohort_avg_par': g.loc[g['is_target']==1,'par'].mean(),
    'noncohort_avg_par': g.loc[g['is_target']==0,'par'].mean(),
}))
print(onb_lc.to_string())

# ROI distribution summary for cohort
print("\n--- ROI distribution in cohort ---")
print(df.loc[df['is_target']==1,'roi'].describe())
df.to_csv("/work/analysis_final.csv", index=False)
print("Saved analysis_final.csv")
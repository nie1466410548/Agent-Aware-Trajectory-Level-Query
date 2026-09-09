import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 150

# Load all data
s1 = db.frame(db.query("SELECT * FROM sheet1 ORDER BY \"Promotion Date\", \"Promotion Tertiary Category\", Strategy"))
s2 = db.frame(db.query("SELECT * FROM sheet2 ORDER BY \"Promotion Date\", \"Promotion Tertiary Category\""))

print("Sheet1 shape:", s1.shape)
print("Sheet2 shape:", s2.shape)
print("Sheet1 columns:", list(s1.columns))
print("Sheet2 columns:", list(s2.columns))
print()

# Strategy families
print("Strategies:", sorted(s1['Strategy'].unique()))
print()

# Determine version mapping
strategy_families = {
    'Search Strategy': ('Search Strategy v3.6', 'Search Strategy v3.7'),
    'Caixi Strategy': ('Caixi Strategy v4.8', 'Caixi Strategy v4.9'),
    'Popup Strategy': ('Popup Strategy v2.9', 'Popup Strategy v2.9.1'),
    'Renqun Dongcha Strategy': ('Renqun Dongcha Strategy v3.2', 'Renqun Dongcha Strategy v3.2.1'),
}

# Join sheet1 with sheet2 on date and tertiary category
s1['dt'] = pd.to_datetime(s1['Promotion Date'])
s2['dt'] = pd.to_datetime(s2['Promotion Date'])

# Merge
df = s1.merge(s2, on=['dt', 'Promotion Tertiary Category'], suffixes=('', '_s2'), how='left')
print("Merged shape:", df.shape)
print("Nulls in order fields:", df[['T+0 strategy-guided order count', 'T+0 strategy-guided transaction amount']].isnull().sum())
print()

# Add period and version info
df['period'] = np.where(df['dt'] <= pd.Timestamp('2025-07-03'), 'pre', 'gray')

# Also add Jul1-4 vs Jul5-7
df['period2'] = np.where(df['dt'] <= pd.Timestamp('2025-07-04'), 'pre_jul4', 'gray_jul5')

# Determine strategy family and version
def get_family_version(strat):
    for fam, (old_v, new_v) in strategy_families.items():
        if strat == old_v:
            return fam, 'old'
        if strat == new_v:
            return fam, 'new'
    return 'other', 'other'

fam_ver = df['Strategy'].apply(get_family_version)
df['family'] = [x[0] for x in fam_ver]
df['version'] = [x[1] for x in fam_ver]

print("Period distribution:")
print(df.groupby('period')['Strategy'].value_counts())
print()

# Aggregate metrics per strategy version per period
agg = df.groupby(['family', 'version', 'period']).agg(
    rows=('Strategy', 'count'),
    spend=('Spend (Yuan)', 'sum'),
    impressions=('Impressions', 'sum'),
    clicks=('Clicks', 'sum'),
    orders=('T+0 strategy-guided order count', 'sum'),
    tx_amt=('T+0 strategy-guided transaction amount', 'sum'),
    ctr_w=('Clicks', lambda x: x.sum() / df.loc[x.index, 'Impressions'].sum() if df.loc[x.index, 'Impressions'].sum() > 0 else 0),
    cpc_w=('Spend (Yuan)', lambda x: x.sum() / df.loc[x.index, 'Clicks'].sum() if df.loc[x.index, 'Clicks'].sum() > 0 else 0),
    cpm_w=('Spend (Yuan)', lambda x: x.sum() * 1000 / df.loc[x.index, 'Impressions'].sum() if df.loc[x.index, 'Impressions'].sum() > 0 else 0),
    budutil_avg=('Budget Utilization Rate', 'mean'),
    aov_avg=('T+0 strategy-guided average order value', 'mean')
).reset_index()

print("Aggregate metrics:")
print(agg.to_string())
print()

# ============================================================
# CONTROLLED CATEGORY-LEVEL ANALYSIS
# ============================================================
# For each family, identify categories that were served by old in pre period.
# Then during gray period, some categories moved to new version, some stayed with old.
# Compare: for categories that moved to new, pre metrics vs gray metrics (paired).
# For categories that stayed with old, pre metrics vs gray metrics (control).

results = {}
for fam, (old_v, new_v) in strategy_families.items():
    print(f"\n{'='*60}")
    print(f"FAMILY: {fam}")
    print(f"Old: {old_v}, New: {new_v}")
    
    # Get all categories served by this family in pre period (under old version)
    pre_cats = set(df[(df['family']==fam) & (df['period']=='pre')]['Promotion Tertiary Category'].unique())
    print(f"Categories in pre period: {len(pre_cats)}")
    
    # Categories served by new version in gray period
    new_cats = set(df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray')]['Promotion Tertiary Category'].unique())
    old_gray_cats = set(df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray')]['Promotion Tertiary Category'].unique())
    
    print(f"Categories in new version (gray): {len(new_cats)}")
    print(f"Categories in old version (gray): {len(old_gray_cats)}")
    print(f"Overlap new vs pre: {len(new_cats & pre_cats)}")
    print(f"Overlap old_gray vs pre: {len(old_gray_cats & pre_cats)}")
    
    # For each category that moved to new version, compute pre-period avg metrics (under old version)
    # and gray-period avg metrics (under new version)
    new_cat_metrics = []
    for cat in new_cats:
        pre_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
        gray_rows = df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
        
        if len(pre_rows) == 0 or len(gray_rows) == 0:
            continue
        
        # For multiple pre days, average
        pre_agg = {
            'ctr': pre_rows['Clicks'].sum() / pre_rows['Impressions'].sum() if pre_rows['Impressions'].sum() > 0 else 0,
            'cpc': pre_rows['Spend (Yuan)'].sum() / pre_rows['Clicks'].sum() if pre_rows['Clicks'].sum() > 0 else 0,
            'cpm': pre_rows['Spend (Yuan)'].sum() * 1000 / pre_rows['Impressions'].sum() if pre_rows['Impressions'].sum() > 0 else 0,
            'budget_util': pre_rows['Budget Utilization Rate'].mean(),
            'spend': pre_rows['Spend (Yuan)'].sum(),
            'impressions': pre_rows['Impressions'].sum(),
            'clicks': pre_rows['Clicks'].sum(),
            'orders': pre_rows['T+0 strategy-guided order count'].sum() / len(pre_rows['dt'].unique()),
            'tx_amt': pre_rows['T+0 strategy-guided transaction amount'].sum() / len(pre_rows['dt'].unique()),
            'aov': pre_rows['T+0 strategy-guided average order value'].mean(),
        }
        
        gray_agg = {
            'ctr': gray_rows['Clicks'].sum() / gray_rows['Impressions'].sum() if gray_rows['Impressions'].sum() > 0 else 0,
            'cpc': gray_rows['Spend (Yuan)'].sum() / gray_rows['Clicks'].sum() if gray_rows['Clicks'].sum() > 0 else 0,
            'cpm': gray_rows['Spend (Yuan)'].sum() * 1000 / gray_rows['Impressions'].sum() if gray_rows['Impressions'].sum() > 0 else 0,
            'budget_util': gray_rows['Budget Utilization Rate'].mean(),
            'spend': gray_rows['Spend (Yuan)'].sum(),
            'impressions': gray_rows['Impressions'].sum(),
            'clicks': gray_rows['Clicks'].sum(),
            'orders': gray_rows['T+0 strategy-guided order count'].sum() / len(gray_rows['dt'].unique()),
            'tx_amt': gray_rows['T+0 strategy-guided transaction amount'].sum() / len(gray_rows['dt'].unique()),
            'aov': gray_rows['T+0 strategy-guided average order value'].mean(),
        }
        
        new_cat_metrics.append({
            'category': cat,
            'pre_' + k: v for k, v in pre_agg.items()
        })
        new_cat_metrics[-1].update({
            'gray_' + k: v for k, v in gray_agg.items()
        })
    
    # For categories that stayed with old version
    old_cat_metrics = []
    for cat in old_gray_cats:
        pre_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
        gray_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
        
        if len(pre_rows) == 0 or len(gray_rows) == 0:
            continue
        
        pre_agg = {
            'ctr': pre_rows['Clicks'].sum() / pre_rows['Impressions'].sum() if pre_rows['Impressions'].sum() > 0 else 0,
            'cpc': pre_rows['Spend (Yuan)'].sum() / pre_rows['Clicks'].sum() if pre_rows['Clicks'].sum() > 0 else 0,
            'cpm': pre_rows['Spend (Yuan)'].sum() * 1000 / pre_rows['Impressions'].sum() if pre_rows['Impressions'].sum() > 0 else 0,
            'budget_util': pre_rows['Budget Utilization Rate'].mean(),
            'spend': pre_rows['Spend (Yuan)'].sum(),
            'impressions': pre_rows['Impressions'].sum(),
            'clicks': pre_rows['Clicks'].sum(),
            'orders': pre_rows['T+0 strategy-guided order count'].sum() / len(pre_rows['dt'].unique()),
            'tx_amt': pre_rows['T+0 strategy-guided transaction amount'].sum() / len(pre_rows['dt'].unique()),
            'aov': pre_rows['T+0 strategy-guided average order value'].mean(),
        }
        
        gray_agg = {
            'ctr': gray_rows['Clicks'].sum() / gray_rows['Impressions'].sum() if gray_rows['Impressions'].sum() > 0 else 0,
            'cpc': gray_rows['Spend (Yuan)'].sum() / gray_rows['Clicks'].sum() if gray_rows['Clicks'].sum() > 0 else 0,
            'cpm': gray_rows['Spend (Yuan)'].sum() * 1000 / gray_rows['Impressions'].sum() if gray_rows['Impressions'].sum() > 0 else 0,
            'budget_util': gray_rows['Budget Utilization Rate'].mean(),
            'spend': gray_rows['Spend (Yuan)'].sum(),
            'impressions': gray_rows['Impressions'].sum(),
            'clicks': gray_rows['Clicks'].sum(),
            'orders': pre_rows['T+0 strategy-guided order count'].sum() / len(pre_rows['dt'].unique()),
            'tx_amt': pre_rows['T+0 strategy-guided transaction amount'].sum() / len(pre_rows['dt'].unique()),
            'aov': pre_rows['T+0 strategy-guided average order value'].mean(),
        }
        
        old_cat_metrics.append({
            'category': cat,
            'pre_' + k: v for k, v in pre_agg.items()
        })
        old_cat_metrics[-1].update({
            'gray_' + k: v for k, v in gray_agg.items()
        })
    
    results[fam] = {
        'new_cats': new_cat_metrics,
        'old_cats': old_cat_metrics
    }
    
    print(f"\nNew-version categories (pre->gray, N={len(new_cat_metrics)}):")
    if len(new_cat_metrics) > 0:
        new_df = pd.DataFrame(new_cat_metrics)
        for metric in ['ctr', 'cpc', 'cpm', 'budget_util', 'orders', 'tx_amt', 'aov']:
            pre_mean = new_df[f'pre_{metric}'].mean()
            gray_mean = new_df[f'gray_{metric}'].mean()
            pct_change = (gray_mean - pre_mean) / pre_mean * 100 if pre_mean != 0 else 0
            print(f"  {metric}: pre={pre_mean:.4f}, gray={gray_mean:.4f}, change={pct_change:+.2f}%")
    
    if len(old_cat_metrics) > 0:
        old_df = pd.DataFrame(old_cat_metrics)
        print(f"\nOld-version categories (pre->gray, N={len(old_cat_metrics)}):")
        for metric in ['ctr', 'cpc', 'cpm', 'budget_util', 'orders', 'tx_amt', 'aov']:
            pre_mean = old_df[f'pre_{metric}'].mean()
            gray_mean = old_df[f'gray_{metric}'].mean()
            pct_change = (gray_mean - pre_mean) / pre_mean * 100 if pre_mean != 0 else 0
            print(f"  {metric}: pre={pre_mean:.4f}, gray={gray_mean:.4f}, change={pct_change:+.2f}%")

print("\n\n============================================================")
print("STATISTICAL TESTS: Compare new-version categories vs old-version categories")
print("============================================================")

for fam, res in results.items():
    print(f"\n--- {fam} ---")
    new_df = pd.DataFrame(res['new_cats']) if res['new_cats'] else pd.DataFrame()
    old_df = pd.DataFrame(res['old_cats']) if res['old_cats'] else pd.DataFrame()
    
    if len(new_df) == 0 or len(old_df) == 0:
        print("  Insufficient data for paired comparison")
        continue
    
    for metric in ['ctr', 'cpc', 'cpm', 'budget_util', 'orders', 'tx_amt']:
        new_delta = new_df[f'gray_{metric}'] - new_df[f'pre_{metric}']
        old_delta = old_df[f'gray_{metric}'] - old_df[f'pre_{metric}']
        
        # Mann-Whitney U test (non-parametric, suitable for small samples)
        try:
            stat, p = stats.mannwhitneyu(new_delta, old_delta, alternative='two-sided')
            print(f"  {metric}: MWU stat={stat:.2f}, p={p:.4f}", end="")
            if p < 0.05:
                print(" (*)")
            else:
                print("")
            
            # Also t-test
            t_stat, t_p = stats.ttest_ind(new_delta, old_delta, equal_var=False)
            print(f"    t-test: t={t_stat:.3f}, p={t_p:.4f}")
        except Exception as e:
            print(f"  {metric}: Error - {e}")
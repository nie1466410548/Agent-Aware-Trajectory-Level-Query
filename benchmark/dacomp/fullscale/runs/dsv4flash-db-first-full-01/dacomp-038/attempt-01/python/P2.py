import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 150

s1 = db.frame(db.query("SELECT * FROM sheet1 ORDER BY \"Promotion Date\", \"Promotion Tertiary Category\", Strategy"))
s2 = db.frame(db.query("SELECT * FROM sheet2 ORDER BY \"Promotion Date\", \"Promotion Tertiary Category\""))

s1['dt'] = pd.to_datetime(s1['Promotion Date'])
s2['dt'] = pd.to_datetime(s2['Promotion Date'])
df = s1.merge(s2, on=['dt', 'Promotion Tertiary Category'], suffixes=('', '_s2'), how='left')
print("Merged shape:", df.shape)

strategy_families = {
    'Search Strategy': ('Search Strategy v3.6', 'Search Strategy v3.7'),
    'Caixi Strategy': ('Caixi Strategy v4.8', 'Caixi Strategy v4.9'),
    'Popup Strategy': ('Popup Strategy v2.9', 'Popup Strategy v2.9.1'),
    'Renqun Dongcha Strategy': ('Renqun Dongcha Strategy v3.2', 'Renqun Dongcha Strategy v3.2.1'),
}

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
df['period'] = np.where(df['dt'] <= pd.Timestamp('2025-07-03'), 'pre', 'gray')

def compute_agg(rows):
    imp = rows['Impressions'].sum()
    clk = rows['Clicks'].sum()
    spd = rows['Spend (Yuan)'].sum()
    n_days = len(rows['dt'].unique())
    return {
        'ctr': clk / imp if imp > 0 else 0,
        'cpc': spd / clk if clk > 0 else 0,
        'cpm': spd * 1000 / imp if imp > 0 else 0,
        'budget_util': rows['Budget Utilization Rate'].mean(),
        'orders_pd': rows['T+0 strategy-guided order count'].sum() / n_days,
        'tx_amt_pd': rows['T+0 strategy-guided transaction amount'].sum() / n_days,
        'aov': rows['T+0 strategy-guided average order value'].mean(),
    }

results = {}
for fam, (old_v, new_v) in strategy_families.items():
    print(f"\n{'='*60}\nFAMILY: {fam}")
    new_cats = sorted(set(df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray')]['Promotion Tertiary Category']))
    old_gray_cats = sorted(set(df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray')]['Promotion Tertiary Category']))
    print(f"New-version cats (gray): {len(new_cats)}, Old-version cats (gray): {len(old_gray_cats)}")

    new_cat_metrics, old_cat_metrics = [], []
    for cat in new_cats:
        pre_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
        gray_rows = df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
        if len(pre_rows) == 0 or len(gray_rows) == 0:
            continue
        rec = {'category': cat}
        rec.update({'pre_' + k: v for k, v in compute_agg(pre_rows).items()})
        rec.update({'gray_' + k: v for k, v in compute_agg(gray_rows).items()})
        new_cat_metrics.append(rec)

    for cat in old_gray_cats:
        pre_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
        gray_rows = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
        if len(pre_rows) == 0 or len(gray_rows) == 0:
            continue
        rec = {'category': cat}
        rec.update({'pre_' + k: v for k, v in compute_agg(pre_rows).items()})
        rec.update({'gray_' + k: v for k, v in compute_agg(gray_rows).items()})
        old_cat_metrics.append(rec)

    results[fam] = {'new_cats': new_cat_metrics, 'old_cats': old_cat_metrics}

    for grp_name, grp in [('NEW (moved cats)', new_cat_metrics), ('OLD (control cats)', old_cat_metrics)]:
        print(f"\n  {grp_name}  N={len(grp)}")
        if not grp:
            continue
        gdf = pd.DataFrame(grp)
        for metric in ['ctr', 'cpc', 'cpm', 'budget_util', 'orders_pd', 'tx_amt_pd', 'aov']:
            pre = gdf[f'pre_{metric}'].mean()
            g = gdf[f'gray_{metric}'].mean()
            pct = (g - pre) / pre * 100 if pre != 0 else 0
            print(f"    {metric:12s}: pre={pre:.4f} gray={g:.4f}  Δ={g-pre:+.4f} ({pct:+.1f}%)")

print("\n\n=== STATISTICAL TESTS: new-version deltas vs old-version deltas ===")
for fam, res in results.items():
    print(f"\n--- {fam} ---")
    new_df = pd.DataFrame(res['new_cats']) if res['new_cats'] else pd.DataFrame()
    old_df = pd.DataFrame(res['old_cats']) if res['old_cats'] else pd.DataFrame()
    if len(new_df) == 0 or len(old_df) == 0:
        print("  Insufficient data for comparison")
        continue
    for metric in ['ctr', 'cpc', 'cpm', 'budget_util', 'orders_pd', 'tx_amt_pd', 'aov']:
        new_delta = new_df[f'gray_{metric}'] - new_df[f'pre_{metric}']
        old_delta = old_df[f'gray_{metric}'] - old_df[f'pre_{metric}']
        try:
            stat, p = stats.mannwhitneyu(new_delta, old_delta, alternative='two-sided')
            t_stat, t_p = stats.ttest_ind(new_delta, old_delta, equal_var=False)
            flag = " *" if p < 0.05 else ""
            print(f"  {metric:12s}: MWU p={p:.4f}{flag} | t-test p={t_p:.4f} | meanΔ new={new_delta.mean():+.4f}, old={old_delta.mean():+.4f}")
        except Exception as e:
            print(f"  {metric}: {e}")
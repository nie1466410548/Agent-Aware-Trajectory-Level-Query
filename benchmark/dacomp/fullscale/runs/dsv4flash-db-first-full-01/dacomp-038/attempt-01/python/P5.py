import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.rcParams['figure.dpi'] = 150
import matplotlib.pyplot as plt

s1 = db.frame(db.query("SELECT * FROM sheet1"))
s2 = db.frame(db.query("SELECT * FROM sheet2"))
s1['dt'] = pd.to_datetime(s1['Promotion Date'])
s2['dt'] = pd.to_datetime(s2['Promotion Date'])
s2 = s2.drop_duplicates(subset=['dt', 'Promotion Tertiary Category'])
df = s1.merge(s2, on=['dt', 'Promotion Tertiary Category'], how='left', suffixes=('', '_s2'))

# Strategy families
sf = {
    'Search': ('Search Strategy v3.6', 'Search Strategy v3.7'),
    'Caixi (Guess You Like)': ('Caixi Strategy v4.8', 'Caixi Strategy v4.9'),
    'Popup': ('Popup Strategy v2.9', 'Popup Strategy v2.9.1'),
    'Renqun Dongcha': ('Renqun Dongcha Strategy v3.2', 'Renqun Dongcha Strategy v3.2.1'),
}
def get_fv(s):
    for fam,(o,n) in sf.items():
        if s==o: return fam,'old'
        if s==n: return fam,'new'
    return 'other','other'
fv = df['Strategy'].apply(get_fv)
df['family']=[x[0] for x in fv]; df['version']=[x[1] for x in fv]
df['period'] = np.where(df['dt'] <= pd.Timestamp('2025-07-03'), 'pre', 'gray')

# For each family, compute per-category pre and gray weighted metrics
def weighted_metrics(rows):
    imp = rows['Impressions'].sum()
    clk = rows['Clicks'].sum()
    spd = rows['Spend (Yuan)'].sum()
    n_days = len(rows['dt'].unique())
    return {
        'impressions': imp,
        'clicks': clk,
        'spend': spd,
        'ctr': clk / imp if imp > 0 else 0,
        'cpc': spd / clk if clk > 0 else 0,
        'cpm': spd * 1000 / imp if imp > 0 else 0,
        'orders_pd': rows['T+0 strategy-guided order count'].sum() / n_days,
        'tx_amt_pd': rows['T+0 strategy-guided transaction amount'].sum() / n_days,
    }

all_results = []
for fam, (old_v, new_v) in sf.items():
    new_cats = sorted(set(df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray')]['Promotion Tertiary Category']))
    old_cats = sorted(set(df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray')]['Promotion Tertiary Category']))
    
    print(f"\n{'='*60}\n{fam}")
    print(f"New-groups (N={len(new_cats)}): {new_cats}")
    print(f"Old-groups (N={len(old_cats)}): {old_cats}")
    
    for grp_name, cats in [('new', new_cats), ('old', old_cats)]:
        per_cat = []
        for cat in cats:
            if grp_name == 'new':
                pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
                gray = df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
            else:
                pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
                gray = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
            if len(pre) == 0 or len(gray) == 0:
                continue
            rec = {'category': cat}
            for k, v in weighted_metrics(pre).items():
                rec['pre_' + k] = v
            for k, v in weighted_metrics(gray).items():
                rec['gray_' + k] = v
            per_cat.append(rec)
        
        if per_cat:
            pdf = pd.DataFrame(per_cat)
            print(f"\n  {grp_name.upper()} group (N={len(per_cat)})")
            # Overall weighted metrics for display
            pre_imp = pdf['pre_impressions'].sum()
            pre_clk = pdf['pre_clicks'].sum()
            pre_spd = pdf['pre_spend'].sum()
            gray_imp = pdf['gray_impressions'].sum()
            gray_clk = pdf['gray_clicks'].sum()
            gray_spd = pdf['gray_spend'].sum()
            
            pre_ctr = pre_clk / pre_imp if pre_imp else 0
            gray_ctr = gray_clk / gray_imp if gray_imp else 0
            pre_cpc = pre_spd / pre_clk if pre_clk else 0
            gray_cpc = gray_spd / gray_clk if gray_clk else 0
            pre_cpm = pre_spd * 1000 / pre_imp if pre_imp else 0
            gray_cpm = gray_spd * 1000 / gray_imp if gray_imp else 0
            
            print(f"    CTR: pre={pre_ctr:.4f} gray={gray_ctr:.4f}  Δ={(gray_ctr-pre_ctr)/pre_ctr*100 if pre_ctr else 0:+.1f}%")
            print(f"    CPC: pre={pre_cpc:.4f} gray={gray_cpc:.4f}  Δ={(gray_cpc-pre_cpc)/pre_cpc*100 if pre_cpc else 0:+.1f}%")
            print(f"    CPM: pre={pre_cpm:.2f} gray={gray_cpm:.2f}  Δ={(gray_cpm-pre_cpm)/pre_cpm*100 if pre_cpm else 0:+.1f}%")
            
            pre_orders = pdf['pre_orders_pd'].sum()
            gray_orders = pdf['gray_orders_pd'].sum()
            print(f"    Orders/day: pre={pre_orders:.0f} gray={gray_orders:.0f}  Δ={(gray_orders-pre_orders)/pre_orders*100 if pre_orders else 0:+.1f}%")
            pre_tx = pdf['pre_tx_amt_pd'].sum()
            gray_tx = pdf['gray_tx_amt_pd'].sum()
            print(f"    Tx amt/day: pre={pre_tx:.0f} gray={gray_tx:.0f}  Δ={(gray_tx-pre_tx)/pre_tx*100 if pre_tx else 0:+.1f}%")
            
            all_results.append({'family': fam, 'group': grp_name, 'N': len(per_cat), 'pdf': pdf})

# Now do the main statistical tests per family
print("\n\n=== STATISTICAL TESTS (per-category deltas: new vs old) ===")
test_results = []
for fam in ['Search', 'Caixi (Guess You Like)', 'Popup', 'Renqun Dongcha']:
    print(f"\n--- {fam} ---")
    new_pdf = None
    old_pdf = None
    for r in all_results:
        if r['family'] == fam and r['group'] == 'new':
            new_pdf = r['pdf']
        if r['family'] == fam and r['group'] == 'old':
            old_pdf = r['pdf']
    
    if new_pdf is None or old_pdf is None or len(new_pdf) == 0 or len(old_pdf) == 0:
        print("  Insufficient data")
        continue
    
    for metric, label in [('ctr', 'CTR'), ('cpc', 'CPC'), ('cpm', 'CPM'), ('orders_pd', 'Orders/day'), ('tx_amt_pd', 'Tx Amt/day')]:
        new_delta = new_pdf[f'gray_{metric}'] - new_pdf[f'pre_{metric}']
        old_delta = old_pdf[f'gray_{metric}'] - old_pdf[f'pre_{metric}']
        
        try:
            mw_stat, mw_p = stats.mannwhitneyu(new_delta, old_delta, alternative='two-sided')
            t_stat, t_p = stats.ttest_ind(new_delta, old_delta, equal_var=False)
            sig = " *" if mw_p < 0.05 else ""
            print(f"  {label:12s}: MWU p={mw_p:.4f}{sig} | t-test p={t_p:.4f} | meanΔ new={new_delta.mean():+.4f} old={old_delta.mean():+.4f}")
            test_results.append({'family': fam, 'metric': label, 'MWU_p': round(mw_p, 4), 't_p': round(t_p, 4), 'sig': mw_p < 0.05, 'new_delta_mean': round(new_delta.mean(), 4), 'old_delta_mean': round(old_delta.mean(), 4)})
        except Exception as e:
            print(f"  {label}: {e}")

# Generate visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Controlled Comparison: New vs Old Strategy Versions\n(Deltas: Gray Period - Pre-Period, per-category averages)', fontsize=14)

for idx, fam in enumerate(['Search', 'Caixi (Guess You Like)', 'Popup', 'Renqun Dongcha']):
    ax = axes[idx // 2][idx % 2]
    new_pdf = old_pdf = None
    for r in all_results:
        if r['family'] == fam and r['group'] == 'new': new_pdf = r['pdf']
        if r['family'] == fam and r['group'] == 'old': old_pdf = r['pdf']
    
    metrics_to_plot = ['ctr', 'cpc', 'cpm', 'orders_pd', 'tx_amt_pd']
    x_pos = np.arange(len(metrics_to_plot))
    width = 0.35
    new_means = []
    old_means = []
    for m in metrics_to_plot:
        if new_pdf is not None and len(new_pdf) > 0:
            new_d = new_pdf[f'gray_{m}'] - new_pdf[f'pre_{m}']
            # Normalize by pre mean for percentage comparison
            pre_mean = new_pdf[f'pre_{m}'].mean()
            new_means.append(new_d.mean() / pre_mean * 100 if pre_mean != 0 else 0)
        else:
            new_means.append(0)
        if old_pdf is not None and len(old_pdf) > 0:
            old_d = old_pdf[f'gray_{m}'] - old_pdf[f'pre_{m}']
            pre_mean = old_pdf[f'pre_{m}'].mean()
            old_means.append(old_d.mean() / pre_mean * 100 if pre_mean != 0 else 0)
        else:
            old_means.append(0)
    
    ax.bar(x_pos - width/2, new_means, width, label='New version', color='steelblue', alpha=0.8)
    ax.bar(x_pos + width/2, old_means, width, label='Old version (control)', color='salmon', alpha=0.8)
    ax.axhline(y=0, color='grey', linestyle='-', linewidth=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(['CTR', 'CPC', 'CPM', 'Orders/day', 'Tx Amt/day'], fontsize=8)
    ax.set_ylabel('% Change from Pre Period', fontsize=9)
    ax.set_title(fam, fontsize=11)
    ax.legend(fontsize=7)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/controlled_comparison.png', dpi=150)
print("\nSaved /work/controlled_comparison.png")

# Market trend figure
fig2, ax2 = plt.subplots(figsize=(10, 5))
daily2 = s2.groupby('dt').agg(
    orders=('T+0 strategy-guided order count', 'sum'),
    tx_amt=('T+0 strategy-guided transaction amount', 'sum')
).reset_index()
daily2['dow'] = daily2['dt'].dt.day_name()
ax2_twin = ax2.twinx()
ax2.plot(daily2['dt'], daily2['orders'], 'o-', color='steelblue', label='Total Orders', linewidth=2, markersize=8)
ax2_twin.plot(daily2['dt'], daily2['tx_amt'], 's-', color='darkorange', label='Total Transaction Amount', linewidth=2, markersize=8)
ax2.axvspan(pd.Timestamp('2025-07-04'), pd.Timestamp('2025-07-07'), alpha=0.1, color='green', label='Gray Release Period')
ax2.axvline(x=pd.Timestamp('2025-07-05'), color='red', linestyle='--', alpha=0.5, label='Jul 5 (Task Reference)')
for _, row in daily2.iterrows():
    ax2.annotate(row['dow'], (row['dt'], row['orders']), textcoords="offset points", xytext=(0,10), fontsize=8, ha='center')
ax2.set_xlabel('Date')
ax2.set_ylabel('Total Orders', color='steelblue')
ax2_twin.set_ylabel('Total Transaction Amount (Yuan)', color='darkorange')
ax2.set_title('Market-Wide Daily Trends (All Categories from Sheet2)', fontsize=13)
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1+lines2, labels1+labels2, fontsize=9)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/market_trends.png', dpi=150)
print("Saved /work/market_trends.png")

# Per-family daily CTR/CPC trends
fig3, axes3 = plt.subplots(2, 2, figsize=(14, 10))
fig3.suptitle('Daily CTR Trend by Strategy Version', fontsize=14)
for idx, fam in enumerate(['Search', 'Caixi (Guess You Like)', 'Popup', 'Renqun Dongcha']):
    ax = axes3[idx // 2][idx % 2]
    for ver, color, marker in [('old', 'salmon', 'o'), ('new', 'steelblue', 's')]:
        g = df[(df['family']==fam) & (df['version']==ver)]
        daily = g.groupby('dt').apply(lambda x: x['Clicks'].sum()/x['Impressions'].sum() if x['Impressions'].sum() > 0 else 0).reset_index()
        daily.columns = ['dt', 'ctr']
        ax.plot(daily['dt'], daily['ctr'], f'{marker}-', color=color, label=ver, markersize=6)
    ax.axvline(x=pd.Timestamp('2025-07-05'), color='red', linestyle='--', alpha=0.3)
    ax.set_title(fam, fontsize=11)
    ax.set_ylabel('CTR', fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/daily_ctr_trend.png', dpi=150)
print("Saved /work/daily_ctr_trend.png")

print("\nDone with analysis.")
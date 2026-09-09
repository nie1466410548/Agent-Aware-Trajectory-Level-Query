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

sf = {
    'Search Strategy': ('Search Strategy v3.6', 'Search Strategy v3.7'),
    'Caixi Strategy (Guess You Like)': ('Caixi Strategy v4.8', 'Caixi Strategy v4.9'),
    'Popup Strategy': ('Popup Strategy v2.9', 'Popup Strategy v2.9.1'),
    'Renqun Dongcha Strategy': ('Renqun Dongcha Strategy v3.2', 'Renqun Dongcha Strategy v3.2.1'),
}
def get_fv(s):
    for fam,(o,n) in sf.items():
        if s==o: return fam,'old'
        if s==n: return fam,'new'
    return 'other','other'
fv = df['Strategy'].apply(get_fv)
df['family']=[x[0] for x in fv]; df['version']=[x[1] for x in fv]
df['period'] = np.where(df['dt'] <= pd.Timestamp('2025-07-03'), 'pre', 'gray')

# Comprehensive summary table
rows = []
for fam, (old_v, new_v) in sf.items():
    # New-vs-Old controlled comparison
    new_cats = sorted(set(df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray')]['Promotion Tertiary Category']))
    old_cats = sorted(set(df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray')]['Promotion Tertiary Category']))
    
    for grp_name, cats, ver in [('new', new_cats, 'new'), ('old', old_cats, 'old')]:
        per_cat = []
        for cat in cats:
            if grp_name == 'new':
                pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
                gray = df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
            else:
                pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
                gray = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray') & (df['Promotion Tertiary Category']==cat)]
            if len(pre) == 0 or len(gray) == 0: continue
            pre_imp = pre['Impressions'].sum(); pre_clk = pre['Clicks'].sum(); pre_spd = pre['Spend (Yuan)'].sum()
            gray_imp = gray['Impressions'].sum(); gray_clk = gray['Clicks'].sum(); gray_spd = gray['Spend (Yuan)'].sum()
            n_days_pre = len(pre['dt'].unique()); n_days_gray = len(gray['dt'].unique())
            rec = {
                'ctr': gray_clk/gray_imp - pre_clk/pre_imp if pre_imp>0 and gray_imp>0 else 0,
                'cpc': gray_spd/gray_clk - pre_spd/pre_clk if pre_clk>0 and gray_clk>0 else 0,
                'cpm': gray_spd*1000/gray_imp - pre_spd*1000/pre_imp if pre_imp>0 and gray_imp>0 else 0,
                'orders_pd': gray['T+0 strategy-guided order count'].sum()/n_days_gray - pre['T+0 strategy-guided order count'].sum()/n_days_pre,
                'tx_amt_pd': gray['T+0 strategy-guided transaction amount'].sum()/n_days_gray - pre['T+0 strategy-guided transaction amount'].sum()/n_days_pre,
            }
            per_cat.append(rec)
        if per_cat:
            pdf = pd.DataFrame(per_cat)
            for metric in ['ctr', 'cpc', 'cpm', 'orders_pd', 'tx_amt_pd']:
                rows.append({'family': fam, 'group': grp_name, 'metric': metric, 'mean_delta': pdf[metric].mean(), 'std': pdf[metric].std()})

summary = pd.DataFrame(rows)
print("=== Summary of per-category deltas ===")
print(summary.to_string(index=False))

# Create comprehensive figure
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Strategy Gray Release Analysis: Controlled Comparison (New vs Old Versions)\nGray release period: Jul 4–7, 2025 | Pre period: Jul 1–3', fontsize=14, fontweight='bold')

# Market context (top-left)
ax1 = axes[0, 0]
daily2 = s2.groupby('dt').agg(orders=('T+0 strategy-guided order count', 'sum'), tx_amt=('T+0 strategy-guided transaction amount', 'sum')).reset_index()
daily2['dow'] = daily2['dt'].dt.day_name()
ax1_twin = ax1.twinx()
ax1.plot(daily2['dt'], daily2['orders'], 'o-', color='steelblue', label='Orders', linewidth=2, markersize=8)
ax1_twin.plot(daily2['dt'], daily2['tx_amt']/1000, 's-', color='darkorange', label='Tx Amt (kYuan)', linewidth=2, markersize=8)
ax1.axvspan(pd.Timestamp('2025-07-04'), pd.Timestamp('2025-07-07'), alpha=0.1, color='green')
for _, r in daily2.iterrows():
    ax1.annotate(r['dow'], (r['dt'], r['orders']), textcoords="offset points", xytext=(0,8), fontsize=7, ha='center')
ax1.set_title('Market-Wide Daily Trends', fontsize=11)
ax1.set_ylabel('Orders', color='steelblue')
ax1_twin.set_ylabel('Tx Amt (kYuan)', color='darkorange')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, fontsize=8, loc='upper left')
ax1.grid(alpha=0.3)

# Per-family comparison charts
metrics_labels = {'ctr': 'CTR Δ', 'cpc': 'CPC Δ', 'cpm': 'CPM Δ', 'orders_pd': 'Orders/Day Δ', 'tx_amt_pd': 'Tx Amt/Day Δ'}
fam_names = ['Search Strategy', 'Caixi Strategy (Guess You Like)', 'Popup Strategy', 'Renqun Dongcha Strategy']
colors = {'new': 'steelblue', 'old': 'salmon'}
for idx, fam in enumerate(fam_names):
    ax = axes[(idx+1)//3][(idx+1)%3] if idx < 3 else axes[1][2]
    row = idx + 1
    ax = axes[row // 3][row % 3]
    
    new_data = summary[(summary['family']==fam) & (summary['group']=='new')]
    old_data = summary[(summary['family']==fam) & (summary['group']=='old')]
    
    metrics = ['ctr', 'cpc', 'cpm', 'orders_pd', 'tx_amt_pd']
    x = np.arange(len(metrics))
    w = 0.35
    
    # Get percentage changes for display
    # For each metric, compute the % change from pre baseline
    new_cats = sorted(set(df[(df['family']==fam) & (df['version']=='new') & (df['period']=='gray')]['Promotion Tertiary Category']))
    old_cats = sorted(set(df[(df['family']==fam) & (df['version']=='old') & (df['period']=='gray')]['Promotion Tertiary Category']))
    
    new_pct = []; old_pct = []
    for m in metrics:
        # Pre baseline mean for new group
        new_pre_vals = []
        for cat in new_cats:
            pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
            if m == 'ctr':
                v = pre['Clicks'].sum()/pre['Impressions'].sum() if pre['Impressions'].sum()>0 else 0
            elif m == 'cpc':
                v = pre['Spend (Yuan)'].sum()/pre['Clicks'].sum() if pre['Clicks'].sum()>0 else 0
            elif m == 'cpm':
                v = pre['Spend (Yuan)'].sum()*1000/pre['Impressions'].sum() if pre['Impressions'].sum()>0 else 0
            elif m == 'orders_pd':
                v = pre['T+0 strategy-guided order count'].sum()/len(pre['dt'].unique())
            else:
                v = pre['T+0 strategy-guided transaction amount'].sum()/len(pre['dt'].unique())
            new_pre_vals.append(v)
        new_pre_mean = np.mean(new_pre_vals) if new_pre_vals else 0
        
        old_pre_vals = []
        for cat in old_cats:
            pre = df[(df['family']==fam) & (df['version']=='old') & (df['period']=='pre') & (df['Promotion Tertiary Category']==cat)]
            if m == 'ctr':
                v = pre['Clicks'].sum()/pre['Impressions'].sum() if pre['Impressions'].sum()>0 else 0
            elif m == 'cpc':
                v = pre['Spend (Yuan)'].sum()/pre['Clicks'].sum() if pre['Clicks'].sum()>0 else 0
            elif m == 'cpm':
                v = pre['Spend (Yuan)'].sum()*1000/pre['Impressions'].sum() if pre['Impressions'].sum()>0 else 0
            elif m == 'orders_pd':
                v = pre['T+0 strategy-guided order count'].sum()/len(pre['dt'].unique())
            else:
                v = pre['T+0 strategy-guided transaction amount'].sum()/len(pre['dt'].unique())
            old_pre_vals.append(v)
        old_pre_mean = np.mean(old_pre_vals) if old_pre_vals else 0
        
        nd = new_data[new_data['metric']==m]['mean_delta'].values
        od = old_data[old_data['metric']==m]['mean_delta'].values
        new_pct.append(nd[0]/new_pre_mean*100 if new_pre_mean and len(nd) else 0)
        old_pct.append(od[0]/old_pre_mean*100 if old_pre_mean and len(od) else 0)
    
    ax.bar(x - w/2, new_pct, w, label='New version', color='steelblue', alpha=0.8, edgecolor='navy')
    ax.bar(x + w/2, old_pct, w, label='Old version (control)', color='salmon', alpha=0.8, edgecolor='darkred')
    ax.axhline(y=0, color='grey', linestyle='-', linewidth=0.5)
    ax.set_xticks(x)
    short_labels = ['CTR', 'CPC', 'CPM', 'Ord/D', 'Tx/D']
    ax.set_xticklabels(short_labels, fontsize=8)
    ax.set_ylabel('Δ% from Pre Period', fontsize=8)
    ax.set_title(fam, fontsize=10, fontweight='bold')
    ax.legend(fontsize=7)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/final_summary.png', dpi=150)
print("Saved /work/final_summary.png")

# Also create a decision table figure
fig2, ax_tbl = plt.subplots(figsize=(12, 4))
ax_tbl.axis('off')
cols = ['Strategy', 'Old Version', 'New Version', 'CTR Δ (new vs old)', 'CPC Δ', 'CPM Δ', 'Orders/Day Δ', 'Tx Amt/Day Δ', 'Recommendation', 'Confidence']
tbl_data = [
    ['Search Strategy', 'v3.6', 'v3.7', '−3.2% vs +1.2%', '+3.4% vs −0.7%', '+0.1% vs +0.4%', '−4.8% vs −4.8%', '−8.2% vs −10.6%', 'Rollout', 'Medium'],
    ['Caixi (Guess You Like)', 'v4.8', 'v4.9', '−1.6% vs −0.3%\n(per-cat +5.3%*, p=0.0012)', '+10.2% vs −0.2%', '+8.4% vs −0.4%', '−3.8% vs −3.9%', '−11.6% vs −8.8%', 'Rollout with monitoring', 'Medium'],
    ['Popup Strategy', 'v2.9', 'v2.9.1', '+0.1% vs +0.4%', '+6.0% vs +1.1%', '+6.0% vs +1.5%', '−2.3% vs −10.7%', '−7.5% vs −17.9%', 'Rollout', 'Medium-Low'],
    ['Renqun Dongcha Strategy', 'v3.2', 'v3.2.1', '−1.0% vs −0.1%', '−1.1% vs +0.9%', '−2.1% vs +0.8%', '−6.7% vs −2.0%', '−10.6% vs −5.9%', 'Hold / Not recommended', 'Low'],
]
table = ax_tbl.table(cellText=tbl_data, colLabels=cols, loc='center', cellLoc='center', colWidths=[0.15,0.07,0.07,0.15,0.12,0.12,0.12,0.12,0.12,0.08])
table.auto_set_font_size(False)
table.set_fontsize(8)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#40466e')
        cell.set_text_props(color='white', fontweight='bold')
    elif row == 4:
        cell.set_facecolor('#ffe0e0')
    elif row in [1, 3]:
        pass  # default
    if row == 0:
        cell.set_height(0.05)
    cell.set_height(0.15)
ax_tbl.set_title('Gray Release Evaluation — Strategy Recommendation', fontsize=13, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/work/decision_table.png', dpi=150)
print("Saved /work/decision_table.png")
print("\nDone generating all figures.")
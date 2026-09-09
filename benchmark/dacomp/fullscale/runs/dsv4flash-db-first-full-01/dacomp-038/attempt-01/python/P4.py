import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.rcParams['figure.dpi'] = 150

s1 = db.frame(db.query("SELECT * FROM sheet1 ORDER BY \"Promotion Date\""))
s2 = db.frame(db.query("SELECT * FROM sheet2 ORDER BY \"Promotion Date\""))
s1['dt'] = pd.to_datetime(s1['Promotion Date'])
s2['dt'] = pd.to_datetime(s2['Promotion Date'])

# dedupe sheet2 (Cocktail on Jul3 appears twice)
s2 = s2.drop_duplicates(subset=['dt', 'Promotion Tertiary Category'])

df = s1.merge(s2, on=['dt', 'Promotion Tertiary Category'], how='left', suffixes=('', '_s2'))
print("Merged shape (deduped):", df.shape)

strategy_families = {
    'Search': ('Search Strategy v3.6', 'Search Strategy v3.7'),
    'Caixi (Guess You Like)': ('Caixi Strategy v4.8', 'Caixi Strategy v4.9'),
    'Popup': ('Popup Strategy v2.9', 'Popup Strategy v2.9.1'),
    'Renqun Dongcha': ('Renqun Dongcha Strategy v3.2', 'Renqun Dongcha Strategy v3.2.1'),
}
def get_fv(s):
    for fam,(o,n) in strategy_families.items():
        if s==o: return fam,'old'
        if s==n: return fam,'new'
    return 'other','other'
fv = df['Strategy'].apply(get_fv)
df['family']=[x[0] for x in fv]; df['version']=[x[1] for x in fv]
df['period'] = np.where(df['dt'] <= pd.Timestamp('2025-07-03'), 'pre', 'gray')
df['day'] = df['dt'].dt.day

# Recompute aggregate
agg_rows=[]
for (fam, ver, per), g in df.groupby(['family','version','period']):
    imp=g['Impressions'].sum(); clk=g['Clicks'].sum(); spd=g['Spend (Yuan)'].sum()
    agg_rows.append({
        'family':fam,'version':ver,'period':per,'rows':len(g),
        'spend':round(spd,0),'impressions':int(imp),'clicks':int(clk),
        'CTR_w':round(clk/imp,4) if imp>0 else 0,
        'CPC_w':round(spd/clk,3) if clk>0 else 0,
        'CPM_w':round(spd*1000/imp,2) if imp>0 else 0,
        'budget_util':round(g['Budget Utilization Rate'].mean(),4),
        'orders':int(g['T+0 strategy-guided order count'].sum()),
        'tx_amt':round(g['T+0 strategy-guided transaction amount'].sum(),0),
    })
agg = pd.DataFrame(agg_rows)
print("\n=== Aggregate by family/version/period (correct boundaries) ===")
print(agg.to_string(index=False))

# Direct old vs new in gray period
print("\n=== DIRECT old vs new within gray period (Jul 4-7) ===")
for fam in ['Search','Caixi (Guess You Like)','Popup','Renqun Dongcha']:
    g = df[(df['family']==fam) & (df['period']=='gray')]
    o = g[g['version']=='old']; n = g[g['version']=='new']
    def metrics(x):
        imp=x['Impressions'].sum(); clk=x['Clicks'].sum(); spd=x['Spend (Yuan)'].sum()
        return dict(rows=len(x), spend=round(spd,0), imp=int(imp), clk=int(clk),
                    ctr=round(clk/imp,4) if imp else 0, cpc=round(spd/clk,3) if clk else 0,
                    cpm=round(spd*1000/imp,2) if imp else 0, bu=round(x['Budget Utilization Rate'].mean(),4),
                    orders=int(x['T+0 strategy-guided order count'].sum()),
                    tx=round(x['T+0 strategy-guided transaction amount'].sum(),0))
    print(f"\n{fam}:")
    print("  OLD:", metrics(o))
    print("  NEW:", metrics(n))
    print("  NEW vs OLD: CTR {:.1%} vs {:.1%}, CPC {:.3f} vs {:.3f}, CPM {:.2f} vs {:.2f}, orders {:.0f} vs {:.0f}".format(
        metrics(n)['ctr'], metrics(o)['ctr'], metrics(n)['cpc'], metrics(o)['cpc'],
        metrics(n)['cpm'], metrics(o)['cpm'], metrics(n)['orders'], metrics(o)['orders']))

# Confounders: Target Audience and Delivery Status distribution per version
print("\n=== Target Audience distribution (gray period) ===")
print(pd.crosstab(df[df['period']=='gray']['family'], [df[df['period']=='gray']['version'], df[df['period']=='gray']['Target Audience']]))
print("\n=== Delivery Status distribution ===")
print(df.groupby('period')['Delivery Status'].value_counts())
print(df['Delivery Status'].unique())

# Check per-day metrics by version for each family
print("\n=== Per-day CTR by family/version (rows: dates) ===")
daily = df.groupby(['family','version','day']).apply(lambda g: pd.Series({
    'ctr': g['Clicks'].sum()/g['Impressions'].sum() if g['Impressions'].sum() else 0,
    'cpc': g['Spend (Yuan)'].sum()/g['Clicks'].sum() if g['Clicks'].sum() else 0,
    'orders': g['T+0 strategy-guided order count'].sum(),
})).reset_index()
print(daily.pivot_table(index=['family','version'], columns='day', values='ctr').round(4).to_string())

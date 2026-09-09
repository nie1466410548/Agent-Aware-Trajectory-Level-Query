import json, numpy as np, pandas as pd
from scipy import stats

rows = []
with open('/results/S12.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=['Year','Surface_Supply','Groundwater_Supply','Surf_GW_Ratio','Urbanization_Rate'])
df = df.sort_values('Year').reset_index(drop=True)
print(df.to_string(index=False))

slope, intercept, r, p, se = stats.linregress(df['Year'], df['Surf_GW_Ratio'])
print(f"\nFull period (2005-2018) ratio trend: slope={slope:.4f} per year, r={r:.4f}, p={p:.4f}")
print(f"Overall change: {df['Surf_GW_Ratio'].iloc[0]:.3f} -> {df['Surf_GW_Ratio'].iloc[-1]:.3f} ({(df['Surf_GW_Ratio'].iloc[-1]/df['Surf_GW_Ratio'].iloc[0]-1)*100:.2f}% relative)")

df['Ratio_YoY'] = df['Surf_GW_Ratio'].diff()
df['Urban_YoY'] = df['Urbanization_Rate'].diff()
print("\nYear-over-year changes:")
print(df[['Year','Surf_GW_Ratio','Ratio_YoY','Urbanization_Rate','Urban_YoY']].to_string(index=False))

for label, lo, hi in [('2005-2010',2005,2010),('2011-2014',2011,2014),('2015-2018',2015,2018),('2005-2014',2005,2014)]:
    sub = df[(df['Year']>=lo)&(df['Year']<=hi)]
    s,i,r,p,se = stats.linregress(sub['Year'], sub['Surf_GW_Ratio'])
    print(f"\nSub-period {label}: mean ratio={sub['Surf_GW_Ratio'].mean():.4f}, range=[{sub['Surf_GW_Ratio'].min():.4f},{sub['Surf_GW_Ratio'].max():.4f}], slope={s:.4f}/yr, r={r:.4f}")

r_ratio_urb, p_ratio_urb = stats.pearsonr(df['Surf_GW_Ratio'], df['Urbanization_Rate'])
print(f"\nPearson corr(Surf_GW_Ratio, Urbanization) = {r_ratio_urb:.4f}, p={p_ratio_urb:.4f}")

for col in ['Surface_Supply','Groundwater_Supply']:
    rc, pc = stats.pearsonr(df[col], df['Urbanization_Rate'])
    print(f"Pearson corr({col}, Urbanization) = {rc:.4f}, p={pc:.4f}")

for label, lo, hi in [('2005-2010',2005,2010),('2011-2014',2011,2014),('2015-2018',2015,2018)]:
    sub = df[(df['Year']>=lo)&(df['Year']<=hi)]
    if len(sub)>2:
        rc, pc = stats.pearsonr(sub['Surf_GW_Ratio'], sub['Urbanization_Rate'])
        print(f"Sub-period {label}: corr(ratio,urban)={rc:.4f}, p={pc:.4f}")

rs, ps = stats.spearmanr(df['Surf_GW_Ratio'], df['Urbanization_Rate'])
print(f"Spearman corr(ratio, urban) = {rs:.4f}, p={ps:.4f}")

s_u,i_u,r_u,p_u,se_u = stats.linregress(df['Year'], df['Urbanization_Rate'])
print(f"\nUrbanization trend: slope={s_u:.4f} pp/yr, r={r_u:.4f}")

df.to_csv('/work/china_series.csv', index=False)
print("\nSaved work/china_series.csv")

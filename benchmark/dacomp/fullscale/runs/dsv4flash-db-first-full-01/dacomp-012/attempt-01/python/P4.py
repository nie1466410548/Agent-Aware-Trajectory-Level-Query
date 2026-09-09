import numpy as np, pandas as pd

df = pd.read_json('/work/diamonds_analysis.json')
df['ppc'] = df['price'] / df['carat']
df['bin01'] = np.round(df['carat'] * 10) / 10
fine = df.groupby('bin01').agg(n=('price','count'), avg_ppc=('ppc','mean'), avg_price=('price','mean')).reset_index()
fine = fine[fine['n'] >= 50].sort_values('bin01')
# Show transition rows around 0.5, 1.0, 1.5, 2.0
interesting = fine[(fine['bin01'] >= 0.4) & (fine['bin01'] <= 2.2)]
print(interesting.round(2).to_string(index=False))

# Percent jump in avg ppc across the 0.5/1.0/1.5 boundaries (from just below to just above)
def jump(boundary, tol=0.09):
    below = fine[(fine['bin01'] >= boundary-tol) & (fine['bin01'] < boundary)]
    above = fine[(fine['bin01'] > boundary) & (fine['bin01'] <= boundary+tol)]
    if len(below) and len(above):
        return (above['avg_ppc'].mean()/below['avg_ppc'].mean() - 1)*100
    return None
for b in [0.5, 1.0, 1.5, 2.0]:
    j = jump(b)
    print(f"Avg PPC jump across {b} ct boundary: {j:+.1f}%" if j is not None else f"{b}: n/a")

# Depth / table: compare avg ppc for extreme vs central depth
df['depth_cat'] = pd.cut(df['depth'], bins=[0,58,60,62,64,100], labels=['<58','58-60','60-62','62-64','>64'])
print("\nAvg PPC by depth bucket (whole data):")
print(df.groupby('depth_cat', observed=True)['ppc'].mean().round(2).to_string())
df['tbl_cat'] = pd.cut(df['tbl'], bins=[0,54,56,58,60,62,100], labels=['<54','54-56','56-58','58-60','60-62','>62'])
print("\nAvg PPC by table bucket (whole data):")
print(df.groupby('tbl_cat', observed=True)['ppc'].mean().round(2).to_string())

# Within 0.5-1.0 ct interval to control carat
sub = df[(df['carat'] > 0.5) & (df['carat'] <= 1.0)]
print("\nAvg PPC by depth bucket within 0.51-1.0 ct:")
print(sub.groupby('depth_cat', observed=True)['ppc'].mean().round(2).to_string())
print("\nAvg PPC by table bucket within 0.51-1.0 ct:")
print(sub.groupby('tbl_cat', observed=True)['ppc'].mean().round(2).to_string())

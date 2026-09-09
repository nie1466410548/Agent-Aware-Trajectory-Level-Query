import pandas as pd
df_clean = pd.read_csv('/work/vocational_clean.csv')
df_clean['primary_industry'] = df_clean['Industry'].fillna('Other').str.split(',').str[0].str.strip()
ind_agg = df_clean.groupby('primary_industry')['salary_mid'].agg(['count', 'mean', 'median'])
ind_agg = ind_agg[ind_agg['count'] >= 20].sort_values('mean', ascending=False)
print("=== INDUSTRY BREAKDOWN (primary tag, n>=20) ===")
for idx, row in ind_agg.iterrows():
    print(f"{idx[:45]:45s} n={int(row['count']):5d}, mean={row['mean']:7.0f}, median={row['median']:7.0f}")
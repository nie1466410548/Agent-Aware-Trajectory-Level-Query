import pandas as pd
import numpy as np

df = pd.read_csv('/work/parsed_data.csv')
top10 = pd.read_csv('/work/top10_avg.csv')

# Format the top-10 table for the report
cols = ['Floor Plan', 'Decoration', 'Floor', 'Orientation', 'cnt', 'avg_watch', 'med_watch', 'max_watch', 'avg_show']
report_top10 = top10[cols].copy()
report_top10.columns = ['Floor Plan', 'Decoration', 'Floor', 'Orientation', 'Listings', 'Avg Watch', 'Med Watch', 'Max Watch', 'Avg Showings']
print(report_top10.round(2).to_string(index=False))
report_top10.round(2).to_csv('/work/report_top10.csv', index=False)

# Overall averages
print("\n=== Overall market averages ===")
print(f"Avg Watch Count: {df['Watch Count'].mean():.2f}")
print(f"Avg Showings: {df['Showings'].mean():.2f}")

# Showings factor summary
print("\n=== Showings Summary (mean ± std) ===")
print("\nBy Decoration:")
print(df.groupby('Decoration')['Showings'].agg(['count','mean','std','median']).round(2).to_string())
print("\nBy Orientation:")
print(df.groupby('Orientation')['Showings'].agg(['count','mean','std','median']).round(2).to_string())
print("\nBy Floor Category:")
print(df.groupby('floor_category')['Showings'].agg(['count','mean','std','median']).round(2).to_string())
print("\nBy Bedrooms:")
print(df.groupby('bedrooms')['Showings'].agg(['count','mean','std','median']).round(2).to_string())

# Floor level continuous: correlation with Showings
from scipy import stats
spec = df[df['floor_type']=='specific']
print(f"\nSpearman corr(floor_num, Showings) among specific floors: {stats.spearmanr(spec['floor_num'], spec['Showings'])[0]:.4f}")
print(f"Spearman corr(floor_num, Watch Count) among specific floors: {stats.spearmanr(spec['floor_num'], spec['Watch Count'])[0]:.4f}")

# Check high-watch combos that also have good showings
print("\n=== Top 10 combos with Showings context ===")
print(report_top10[['Floor Plan','Decoration','Floor','Orientation','Listings','Avg Watch','Avg Showings']].round(2).to_string(index=False))

# Also show what share of listings these combos represent
print(f"\nTotal listings in top-10 combos: {report_top10['Listings'].sum()} / 29975 = {report_top10['Listings'].sum()/29975*100:.2f}%")
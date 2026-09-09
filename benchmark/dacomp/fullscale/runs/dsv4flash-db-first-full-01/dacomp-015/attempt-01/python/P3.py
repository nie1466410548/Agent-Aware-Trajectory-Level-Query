import pandas as pd
import numpy as np

df = pd.read_csv('/work/parsed_data.csv')

# Filter complete rows
sub = df[df['Floor Plan'].notna() & df['Decoration'].notna() & df['Floor'].notna() & df['Orientation'].notna()].copy()

# Group by combination
grp = sub.groupby(['Floor Plan', 'Decoration', 'Floor', 'Orientation']).agg(
    cnt=('Watch Count', 'count'),
    avg_watch=('Watch Count', 'mean'),
    med_watch=('Watch Count', 'median'),
    max_watch=('Watch Count', 'max'),
    p75_watch=('Watch Count', lambda x: x.quantile(0.75)),
    avg_show=('Showings', 'mean')
).reset_index()

# Top 10 by average with cnt>=5
top_avg = grp[grp['cnt']>=5].sort_values('avg_watch', ascending=False).head(10)
print("=== TOP 10 by AVG Watch Count (cnt>=5) ===")
print(top_avg.to_string(index=False))

# Top 10 by median with cnt>=5
top_med = grp[grp['cnt']>=5].sort_values('med_watch', ascending=False).head(10)
print("\n=== TOP 10 by MEDIAN Watch Count (cnt>=5) ===")
print(top_med[['Floor Plan','Decoration','Floor','Orientation','cnt','med_watch','avg_watch','p75_watch']].to_string(index=False))

# Top 10 by total watch count (market-level impact)
top_sum = grp[grp['cnt']>=5].assign(total_watch=lambda d: d['avg_watch']*d['cnt']).sort_values('total_watch', ascending=False).head(10)
print("\n=== TOP 10 by TOTAL Watch Count (cnt>=5) ===")
print(top_sum[['Floor Plan','Decoration','Floor','Orientation','cnt','avg_watch','total_watch']].to_string(index=False))

top_avg.to_csv('/work/top10_avg.csv', index=False)
top_med.to_csv('/work/top10_med.csv', index=False)
top_sum.to_csv('/work/top10_sum.csv', index=False)
print("\nSaved.")
import pandas as pd
import numpy as np

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

# Main category virality
print("=== Virality by Main Category (unique videos) ===")
main_viral = df_u.groupby('Main Category').agg(
    cnt=('Views','count'),
    avg_views=('Views','mean'),
    median_views=('Views','median'),
    pct_2m=('Views', lambda x: (x>=2000000).mean()*100),
    pct_1m=('Views', lambda x: (x>=1000000).mean()*100)
).sort_values('pct_2m', ascending=False)
print(main_viral.round(1))

# How many unique videos are 2M+ views, and what's the follower distribution?
viral = df_u[df_u['Views'] >= 2000000]
print(f"\n=== Viral videos (2M+ views): {len(viral)} ===")
print(f"  By creator size:")
for band in ['<10k', '10k-100k', '100k-1M', '>1M']:
    if band == '<10k':
        n = len(viral[viral['Creator Followers'] < 10000])
    elif band == '10k-100k':
        n = len(viral[(viral['Creator Followers'] >= 10000) & (viral['Creator Followers'] < 100000)])
    elif band == '100k-1M':
        n = len(viral[(viral['Creator Followers'] >= 100000) & (viral['Creator Followers'] < 1000000)])
    else:
        n = len(viral[viral['Creator Followers'] >= 1000000])
    print(f"    {band}: {n} ({n/len(viral)*100:.1f}%)")

# What fraction of viral creators have less than 1M followers?
small = viral[viral['Creator Followers'] < 1000000]
print(f"  Viral videos from creators <1M followers: {len(small)} ({len(small)/len(viral)*100:.1f}%)")

# Whole site category analysis (the main ranking)
ws = df_u[df_u['Main Category'] == 'Whole site']
print(f"\n=== Whole-site Ranking (n={len(ws)}) ===")
print(f"  Avg views: {ws['Views'].mean():.0f}")
print(f"  Top categories by views in whole-site ranking:")
ws_cat = ws.groupby('Video Category').agg(cnt=('Views','count'), avg_views=('Views','mean')).query('cnt>=3').sort_values('avg_views', ascending=False).head(10)
print(ws_cat.round(0))

# Top 10 videos overall (by rank)
top10 = df_u[df_u['Rank'] <= 10]
print("\n=== Top 10 Ranked Videos Sample (unique) ===")
for _, row in top10.sort_values('Rank').head(10).iterrows():
    print(f"  Rank {row['Rank']}: Views={row['Views']:>8}, Cat={str(row['Video Category'])[:22]:>22}, Followers={row['Creator Followers']:>8}, {row['Title'][:35]}")
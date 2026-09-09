import pandas as pd
import numpy as np
from collections import Counter

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

# Compute share rate per video and look at top-share videos
df_u['share_rate'] = df_u['Shares'] / df_u['Views'] * 100
df_u['fav_rate'] = df_u['Favorites'] / df_u['Views'] * 100
df_u['like_rate'] = df_u['Likes'] / df_u['Views'] * 100

print("=== Top 15 videos by share rate (unique, count>=1000 views) ===")
top_share = df_u[df_u['Views'] >= 100000].sort_values('share_rate', ascending=False).head(15)
for _, row in top_share.iterrows():
    print(f"  Share rate: {row['share_rate']:.2f}%, Views: {row['Views']:>8}, Category: {str(row['Video Category'])[:25]:>25}, Title: {row['Title'][:40]}")

# Which categories have highest average share rate?
cat_share = df_u.groupby('Video Category').agg(
    cnt=('Views','count'),
    avg_share_rate=('share_rate','mean'),
    avg_views=('Views','mean')
).query('cnt>=10').sort_values('avg_share_rate', ascending=False)
print("\n=== Categories with highest avg share rate ===")
print(cat_share.head(10).round(2))

# What about favorites (utility) categories?
cat_fav = df_u.groupby('Video Category').agg(
    cnt=('Views','count'),
    avg_fav_rate=('fav_rate','mean'),
    avg_views=('Views','mean')
).query('cnt>=10').sort_values('avg_fav_rate', ascending=False)
print("\n=== Categories with highest avg favorite rate (utility) ===")
print(cat_fav.head(10).round(2))

# Beginner-viral examples: creators with <10k followers and >1M views - what categories?
beginner_viral = df_u[(df_u['Creator Followers'] < 10000) & (df_u['Views'] >= 1000000)]
print(f"\n=== Beginner viral videos (n={len(beginner_viral)}) category distribution ===")
print(beginner_viral['Video Category'].value_counts().head(10))
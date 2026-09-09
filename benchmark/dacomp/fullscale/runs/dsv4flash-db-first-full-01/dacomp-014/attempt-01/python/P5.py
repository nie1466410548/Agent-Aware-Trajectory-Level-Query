import pandas as pd
import numpy as np

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# De-duplicate to get unique videos (take first occurrence)
df_unique = df.drop_duplicates(subset=['Title','Creator']).copy()
print(f"Unique videos: {len(df_unique)}")

# Small creators who went viral (less than 10k followers, more than 2M views)
small_viral = df_unique[(df_unique['Creator Followers'] < 10000) & (df_unique['Views'] >= 2000000)]
print(f"\nSmall creators (<10k followers) with 2M+ views: {len(small_viral)}")
print(f"Small creators (<10k followers) with 1M+ views: {len(df_unique[(df_unique['Creator Followers'] < 10000) & (df_unique['Views'] >= 1000000)])}")

# Show top 10 small creators who went viral
print("\n=== Top Small Creators who went Viral ===")
cols = ['Title','Creator','Views','Likes','Coins','Shares','Favorites','Video Category','Creator Followers','Creator Video Count']
for _, row in small_viral.sort_values('Views', ascending=False).head(10).iterrows():
    print(f"  Views: {row['Views']:>8}, Followers: {row['Creator Followers']:>7}, Videos: {row['Creator Video Count']:>3}, Category: {str(row['Video Category']):>20}, Creator: {row['Creator'][:20]}")

# Engagement rates by category
cat_engagement = df_unique.groupby('Video Category').agg(
    count=('Views', 'count'),
    avg_views=('Views', 'mean'),
    avg_like_rate=('Likes', lambda x: x.mean()/df_unique.loc[x.index,'Views'].mean()*100),
    avg_coin_rate=('Coins', lambda x: x.mean()/df_unique.loc[x.index,'Views'].mean()*100),
    avg_fav_rate=('Favorites', lambda x: x.mean()/df_unique.loc[x.index,'Views'].mean()*100),
    avg_share_rate=('Shares', lambda x: x.mean()/df_unique.loc[x.index,'Views'].mean()*100),
).query('count >= 10').sort_values('avg_views', ascending=False)

print("\n=== Top 15 Categories by Avg Views (unique videos, count>=10) ===")
print(cat_engagement.head(15).round(2))
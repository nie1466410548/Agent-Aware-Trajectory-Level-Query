import pandas as pd
import numpy as np

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Deduplicate
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

# Beginners: creators with <10k followers or <10 videos
beginners = df_u[df_u['Creator Followers'] < 10000]
print(f"Videos by beginners (<10k followers): {len(beginners)}")

# Categories where beginners succeed most
cat_beg = beginners.groupby('Video Category').agg(
    cnt=('Views','count'),
    avg_views=('Views','mean'),
    median_views=('Views', lambda x: x.median()),
    max_views=('Views','max'),
    avg_followers=('Creator Followers','mean')
).query('cnt >= 5').sort_values('avg_views', ascending=False)

print("\n=== Categories where Beginners (<10k followers) Succeed Most ===")
print(cat_beg.head(15).round(0))

# Categories with highest engagement rates (unique videos, count>=10)
cat_eng = df_u.groupby('Video Category').agg(
    cnt=('Views','count'),
    like_rate=('Likes', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    coin_rate=('Coins', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    fav_rate=('Favorites', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    share_rate=('Shares', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    avg_views=('Views','mean')
).query('cnt >= 10')

print("\n=== Highest Like Rate Categories (engagement quality) ===")
print(cat_eng.sort_values('like_rate', ascending=False).head(15).round(2))

print("\n=== Highest Share Rate Categories (spreadability) ===")
print(cat_eng.sort_values('share_rate', ascending=False).head(15).round(2))

print("\n=== Highest Coin Rate Categories (monetary support) ===")
print(cat_eng.sort_values('coin_rate', ascending=False).head(15).round(2))
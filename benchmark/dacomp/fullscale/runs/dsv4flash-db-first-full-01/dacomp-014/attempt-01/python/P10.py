import pandas as pd
import numpy as np
from collections import Counter

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

# Star category analysis
star = df_u[df_u['Video Category'] == 'star']
print(f"=== Star Category Analysis ({len(star)} videos) ===")
print(f"  Avg views: {star['Views'].mean():.0f}")
print(f"  Median views: {star['Views'].median():.0f}")
print(f"  Avg followers: {star['Creator Followers'].mean():.0f}")
print(f"  Median followers: {star['Creator Followers'].median():.0f}")
print(f"  Avg video count: {star['Creator Video Count'].mean():.0f}")
print(f"  Top creators in star category:")
for _, row in star.sort_values('Views', ascending=False).head(10).iterrows():
    print(f"    Views: {row['Views']:>8}, Followers: {row['Creator Followers']:>7}, Creator: {row['Creator'][:25]}")

# Title length analysis
df_u['title_len'] = df_u['Title'].str.len()
top_viral = df_u[df_u['Views'] >= 2000000]
bottom = df_u[df_u['Views'] < 500000]
print(f"\n=== Title Length Analysis ===")
print(f"  Viral videos (2M+ views): avg title length = {top_viral['title_len'].mean():.1f} chars")
print(f"  Low-view videos (<500k): avg title length = {bottom['title_len'].mean():.1f} chars")

# Brackets/parentheses in titles (e.g., [XXX] style)
pattern = r'[\[\(\{]'
top_viral['has_bracket'] = top_viral['Title'].str.contains(pattern, regex=True)
bottom['has_bracket'] = bottom['Title'].str.contains(pattern, regex=True)
print(f"  Viral videos with brackets in title: {top_viral['has_bracket'].mean()*100:.1f}%")
print(f"  Low-view videos with brackets in title: {bottom['has_bracket'].mean()*100:.1f}%")

# Engagement efficiency: likes/views, coins/views ratio
print(f"\n=== Engagement Efficiency ===")
for rg in ['2M+ views', '1M-2M views', '500k-1M', '<500k']:
    if rg == '2M+ views':
        sub = df_u[df_u['Views'] >= 2000000]
    elif rg == '1M-2M views':
        sub = df_u[(df_u['Views'] >= 1000000) & (df_u['Views'] < 2000000)]
    elif rg == '500k-1M':
        sub = df_u[(df_u['Views'] >= 500000) & (df_u['Views'] < 1000000)]
    else:
        sub = df_u[df_u['Views'] < 500000]
    print(f"  {rg} (n={len(sub)}):")
    print(f"    Like rate: {sub['Likes'].sum()/sub['Views'].sum()*100:.2f}%")
    print(f"    Coin rate: {sub['Coins'].sum()/sub['Views'].sum()*100:.2f}%")
    print(f"    Share rate: {sub['Shares'].sum()/sub['Views'].sum()*100:.2f}%")
    print(f"    Fav rate: {sub['Favorites'].sum()/sub['Views'].sum()*100:.2f}%")
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

# ---- Figure 1: Top categories by average views (unique videos, count>=10) ----
cat_views = df_u.groupby('Video Category').agg(
    cnt=('Views','count'),
    avg_views=('Views','mean')
).query('cnt >= 10').sort_values('avg_views', ascending=False).head(15)

fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Blues(np.linspace(0.4, 0.9, 15))
bars = ax.barh(range(len(cat_views)), cat_views['avg_views'].values/1e6, color=colors[::-1])
ax.set_yticks(range(len(cat_views)))
ax.set_yticklabels(cat_views.index, fontsize=9)
ax.set_xlabel('Average Views (Millions)')
ax.set_title('Top 15 Video Categories by Average Views\n(Monthly Ranking Data, Bilibili)')
for i, (v, c) in enumerate(zip(cat_views['avg_views'].values, cat_views['cnt'].values)):
    ax.text(v/1e6 + 0.05, i, f'{v/1e6:.1f}M (n={c})', va='center', fontsize=8)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('/work/category_avg_views.png', dpi=100)
plt.close()

# ---- Figure 2: Engagement rates comparison ----
df_u['view_group'] = pd.cut(df_u['Views'], bins=[0, 500000, 1000000, 2000000, 100000000], 
                              labels=['<500k', '500k-1M', '1M-2M', '2M+'])
engagement = df_u.groupby('view_group').agg(
    like_rate=('Likes', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    coin_rate=('Coins', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    share_rate=('Shares', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
    fav_rate=('Favorites', lambda x: x.sum()/df_u.loc[x.index,'Views'].sum()*100),
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(engagement))
width = 0.2
metrics = ['like_rate', 'coin_rate', 'share_rate', 'fav_rate']
labels = ['Like Rate', 'Coin Rate', 'Share Rate', 'Favorite Rate']
colors = ['#4e79a7', '#f28e2b', '#e15759', '#59a14f']
for i, (m, l, c) in enumerate(zip(metrics, labels, colors)):
    ax.bar(x + i*width, engagement[m], width, label=l, color=c)
ax.set_xticks(x + width*1.5)
ax.set_xticklabels(engagement['view_group'], fontsize=10)
ax.set_ylabel('Engagement Rate (%)')
ax.set_title('Engagement Rates by View Count Level')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('/work/engagement_rates.png', dpi=100)
plt.close()

# ---- Figure 3: Small creators vs large creators success ----
df_u['creator_size'] = pd.cut(df_u['Creator Followers'], 
                               bins=[0, 10000, 100000, 1000000, 100000000],
                               labels=['<10k', '10k-100k', '100k-1M', '>1M'])
size_views = df_u.groupby('creator_size')['Views'].agg(['count','mean','median']).reset_index()
print(size_views)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(size_views['creator_size'], size_views['mean']/1e6, 
              color=['#1f77b4','#ff7f0e','#2ca02c','#d62728'])
ax.set_xlabel('Creator Follower Count')
ax.set_ylabel('Average Views (Millions)')
ax.set_title('Average Views by Creator Follower Size')
for i, (v, c) in enumerate(zip(size_views['mean'].values, size_views['count'].values)):
    ax.text(i, v/1e6 + 0.05, f'{v/1e6:.1f}M\n(n={c})', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/follower_vs_views.png', dpi=100)
plt.close()

# ---- Figure 4: Correlation heatmap ----
metrics_df = df_u[['Views', 'Likes', 'Coins', 'Favorites', 'Shares', 'Comments', 'Danmaku Count']]
corr = metrics_df.corr(method='spearman')

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
            vmin=0.5, vmax=1.0, center=0.75, square=True, ax=ax)
ax.set_title('Spearman Rank Correlations Between Engagement Metrics', fontsize=12)
plt.tight_layout()
plt.savefig('/work/correlation_heatmap.png', dpi=100)
plt.close()

print("All figures saved successfully.")
print(f"Files in /work: {!r}")
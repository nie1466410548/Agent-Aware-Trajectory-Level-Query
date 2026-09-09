import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)

grp = df.groupby(['Difficulty Level', 'Level Type']).agg(
    level_count=('Level ID', 'count'),
    avg_churn=('Churn Rate', 'mean'),
    avg_rating=('Level Rating', 'mean')
).reset_index()

order_diff = ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']
order_type = ['Exploration', 'Parkour', 'Puzzle', 'Battle', 'BOSS']
grp['Difficulty Level'] = pd.Categorical(grp['Difficulty Level'], categories=order_diff, ordered=True)
grp['Level Type'] = pd.Categorical(grp['Level Type'], categories=order_type, ordered=True)
grp = grp.sort_values(['Difficulty Level', 'Level Type'])

piv_churn = grp.pivot(index='Difficulty Level', columns='Level Type', values='avg_churn').reindex(index=order_diff, columns=order_type)
piv_rating = grp.pivot(index='Difficulty Level', columns='Level Type', values='avg_rating').reindex(index=order_diff, columns=order_type)
piv_cnt = grp.pivot(index='Difficulty Level', columns='Level Type', values='level_count').reindex(index=order_diff, columns=order_type).fillna(0).astype(int)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.heatmap(piv_churn, annot=True, fmt='.3f', cmap='RdYlGn_r', ax=axes[0], cbar_kws={'label': 'Avg Churn Rate'})
axes[0].set_title('Avg Churn Rate (2024 Levels)')
sns.heatmap(piv_rating, annot=True, fmt='.2f', cmap='RdYlGn', ax=axes[1], cbar_kws={'label': 'Avg Level Rating'})
axes[1].set_title('Avg Level Rating (2024 Levels)')
sns.heatmap(piv_cnt, annot=True, fmt='d', cmap='Blues', ax=axes[2], cbar_kws={'label': 'Level Count'})
axes[2].set_title('Level Count (2024 Levels)')
plt.tight_layout()
plt.savefig('work/heatmaps_2024.png', dpi=120)
plt.close()

fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=df, x='Level Rating', y='Churn Rate', hue='Difficulty Level',
                hue_order=order_diff, alpha=0.35, s=18, ax=ax)
ax.set_title('Churn Rate vs Level Rating (2024 Levels)')
plt.tight_layout()
plt.savefig('work/scatter_churn_rating.png', dpi=120)
plt.close()

fig, ax = plt.subplots(figsize=(12, 6))
g = sns.catplot(data=grp, x='Difficulty Level', y='avg_churn', hue='Level Type', 
                kind='bar', palette='Set2', height=5, aspect=1.5, legend_out=False)
g.set_axis_labels('Difficulty Level', 'Avg Churn Rate')
g._legend.set_title('Level Type')
plt.suptitle('Churn Rate by Difficulty & Level Type (2024)', y=1.02)
plt.tight_layout()
plt.savefig('work/bar_churn.png', dpi=120)
plt.close()

fig, ax = plt.subplots(figsize=(12, 6))
g = sns.catplot(data=grp, x='Difficulty Level', y='avg_rating', hue='Level Type', 
                kind='bar', palette='Set2', height=5, aspect=1.5, legend_out=False)
g.set_axis_labels('Difficulty Level', 'Avg Level Rating')
g._legend.set_title('Level Type')
plt.suptitle('Level Rating by Difficulty & Level Type (2024)', y=1.02)
plt.tight_layout()
plt.savefig('work/bar_rating.png', dpi=120)
plt.close()

import os
print(sorted(os.listdir('work')))
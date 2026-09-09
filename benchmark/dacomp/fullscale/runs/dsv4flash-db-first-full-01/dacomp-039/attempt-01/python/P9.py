import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)
order = ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']

fig, ax1 = plt.subplots(figsize=(9, 5.5))
m = df.groupby('Difficulty Level')[['Churn Rate', 'Level Rating']].mean().reindex(order)
x = np.arange(4)
ax1.bar(x - 0.2, m['Churn Rate'], width=0.4, label='Avg Churn Rate', color='#d1495b', alpha=0.85)
ax1.set_ylabel('Avg Churn Rate')
ax1.set_xticks(x); ax1.set_xticklabels(order)
ax2 = ax1.twinx()
ax2.plot(x + 0.2, m['Level Rating'], 'o-', color='#00798c', label='Avg Level Rating', lw=2)
ax2.set_ylabel('Avg Level Rating')
ax1.set_ylim(0, 0.7); ax2.set_ylim(0, 5)
ax1.set_title('Difficulty: Churn Rate vs Level Rating Trade-off (2024 Levels)')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
plt.savefig('work/difficulty_tradeoff.png', dpi=120)
plt.close()

# Quantile table within difficulty for churn to support optimization thresholds
print("Churn quantiles by difficulty (2024):")
print(df.groupby('Difficulty Level')['Churn Rate'].quantile([0.25, 0.5, 0.75, 0.9]).unstack().reindex(order).round(4))
print("\nRating quantiles by difficulty (2024):")
print(df.groupby('Difficulty Level')['Level Rating'].quantile([0.25, 0.5, 0.75]).unstack().reindex(order).round(2))
print("\nParticipating players avg by difficulty:")
print(df.groupby('Difficulty Level')['Number of Participating Players'].mean().reindex(order).round(0))
print("\nLevel counts by type within difficulty (2024):")
print(pd.crosstab(df['Difficulty Level'], df['Level Type']).reindex(order))
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)

print("Correlations with Churn Rate and Level Rating:")
cols = ['Number of Participating Players', 'Average Clear Time (S)', 'Level Completion Rate', 'Clear Rate', 'Average Retry Count', 'Reward Value']
for c in cols:
    print(f"{c:35s} churn r={df['Churn Rate'].corr(df[c]):.4f}, rating r={df['Level Rating'].corr(df[c]):.4f}")

# Summary bubble chart: avg churn vs avg rating per combo
grp = df.groupby(['Difficulty Level', 'Level Type']).agg(
    level_count=('Level ID', 'count'),
    avg_churn=('Churn Rate', 'mean'),
    avg_rating=('Level Rating', 'mean')
).reset_index()
order_diff = ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']
grp['Difficulty Level'] = pd.Categorical(grp['Difficulty Level'], categories=order_diff, ordered=True)

plt.figure(figsize=(10, 7))
for diff in order_diff:
    sub = grp[grp['Difficulty Level'] == diff]
    plt.scatter(sub['avg_rating'], sub['avg_churn'], s=sub['level_count']/3.5,
                label=diff, alpha=0.75, edgecolors='k', linewidths=0.5)
    for _, r in sub.iterrows():
        plt.annotate(r['Level Type'], (r['avg_rating'], r['avg_churn']),
                     textcoords='offset points', xytext=(6, 4), fontsize=9)
plt.xlabel('Avg Level Rating'); plt.ylabel('Avg Churn Rate')
plt.title('2024 Level Combinations: Churn vs Rating (bubble = level count)')
plt.legend(title='Difficulty Level')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/scatter_combo_summary.png', dpi=120)
plt.close()

# Churn distribution by difficulty (violin)
plt.figure(figsize=(9, 6))
sns.violinplot(data=df, x='Difficulty Level', y='Churn Rate', order=order_diff, cut=0)
plt.title('Churn Rate Distribution by Difficulty (2024)')
plt.tight_layout()
plt.savefig('work/violin_churn.png', dpi=120)
plt.close()

print("Summary figures saved.")
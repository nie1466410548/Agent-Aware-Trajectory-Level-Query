import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Get detailed language breakdown for the top 4 surveys
top_surveys = ['SUR10001791916', 'SUR10002490769', 'SUR10000172961', 'SUR10001778080']

all_survey_lang = []
for sid in top_surveys:
    result = db.query(f"""
        SELECT survey_id, user_language, COUNT(*) as n, AVG(value) as avg_v,
               MIN(value) as min_v, MAX(value) as max_v
        FROM qualtrics__response
        WHERE survey_id = '{sid}'
        GROUP BY user_language
    """)
    sdf = db.frame(result)
    all_survey_lang.append(sdf)

survey_lang = pd.concat(all_survey_lang)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, sid in enumerate(top_surveys):
    sdf = survey_lang[survey_lang['survey_id'] == sid].sort_values('avg_v', ascending=False)
    ax = axes[i]
    colors = ['#27ae60' if v > 7 else '#e74c3c' if v < 3 else '#f39c12' for v in sdf['avg_v']]
    bars = ax.bar(sdf['user_language'], sdf['avg_v'], color=colors)
    ax.axhline(y=7, color='green', linestyle='--', alpha=0.5, label='Revenue > $7')
    ax.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Revenue < $3')
    ax.set_title(f'Survey {sid[-4:]} (n={sdf["n"].sum()})')
    ax.set_ylabel('Avg Value (1-10)')
    ax.set_ylim(0, 10)
    ax.legend(fontsize=8)
    
    for j, (_, row) in enumerate(sdf.iterrows()):
        ax.text(j, row['avg_v'] + 0.2, f'{row["avg_v"]:.1f}', ha='center', fontsize=9)

plt.suptitle('Performance Divergence Across Regions in Top Candidate Surveys', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('/work/survey_divergence.png', dpi=150)
print("Figure saved to /work/survey_divergence.png")

# Create overall value distribution by language
result = db.query("""
    SELECT user_language, value
    FROM qualtrics__response
""")
df = db.frame(result)

fig2, ax = plt.subplots(figsize=(12, 6))
lang_order = df.groupby('user_language')['value'].mean().sort_values(ascending=False).index
df_box = df.copy()
df_box['user_language'] = pd.Categorical(df_box['user_language'], categories=lang_order, ordered=True)
bp = df_box.boxplot(column='value', by='user_language', ax=ax, 
                    patch_artist=True, 
                    boxprops=dict(alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))
ax.axhline(y=7, color='green', linestyle='--', alpha=0.7, label='Revenue > $7 threshold')
ax.axhline(y=3, color='red', linestyle='--', alpha=0.7, label='Revenue < $3 threshold')
ax.set_title('Value Distribution by Region (Language)')
ax.set_ylabel('Value (1-10 scale)')
ax.set_xlabel('Region')
ax.legend()
plt.suptitle('')
plt.tight_layout()
plt.savefig('/work/value_distribution.png', dpi=150)
print("Figure saved to /work/value_distribution.png")

# Key statistics
print(f"\nOverall score: {df['value'].mean()*10:.2f}")
print(f"Top market segment (value > 7) score: {df[df['value']>7]['value'].mean()*10:.2f}")
print(f"Low market segment (value < 3) score: {df[df['value']<3]['value'].mean()*10:.2f}")
print(f"Top markets: {len(df[df['value']>7])} ({len(df[df['value']>7])/len(df)*100:.1f}%)")
print(f"Low markets: {len(df[df['value']<3])} ({len(df[df['value']<3])/len(df)*100:.1f}%)")

# Market ranking
lang_rank = df.groupby('user_language').agg(avg_score=('value', 'mean')).sort_values('avg_score', ascending=False)
lang_rank['score'] = lang_rank['avg_score'] * 10
print("\nMarket ranking:")
print(lang_rank.to_string())
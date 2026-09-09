import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Get detailed data for the top 5 divergent surveys
top_surveys = ['SUR10001791916', 'SUR10002490769', 'SUR10000172961', 'SUR10001778080', 'SUR10000650179']

# Get survey names
for sid in top_surveys:
    result = db.query(f"SELECT survey_name, project_category, project_type, count_questions FROM qualtrics__survey WHERE survey_id = '{sid}' LIMIT 1")
    info = db.frame(result)
    result2 = db.query(f"SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = '{sid}'")
    stats = db.frame(result2)
    print(f"{sid}: {info['survey_name'].iloc[0]}, Category={info['project_category'].iloc[0]}, "
          f"Overall Score={stats['avg_val'].iloc[0]*10:.2f}, n={stats['n'].iloc[0]}")

# Get detailed language breakdown for top 5 surveys
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
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for i, sid in enumerate(top_surveys):
    sdf = survey_lang[survey_lang['survey_id'] == sid].sort_values('avg_v', ascending=False)
    ax = axes[i]
    colors = ['#27ae60' if v > 7 else '#e74c3c' if v < 3 else '#f39c12' for v in sdf['avg_v']]
    bars = ax.bar(sdf['user_language'], sdf['avg_v'], color=colors)
    ax.axhline(y=7, color='green', linestyle='--', alpha=0.5, label='Revenue > $7')
    ax.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Revenue < $3')
    ax.set_title(f'Survey {sid[-4:]} (n={sdf["n"].sum()})')
    ax.set_ylabel('Avg Value')
    ax.set_ylim(0, 10)
    ax.legend(fontsize=8)
    
    # Add value labels
    for j, (_, row) in enumerate(sdf.iterrows()):
        ax.text(j, row['avg_v'] + 0.2, f'{row["avg_v"]:.1f}', ha='center', fontsize=9)

# Hide the 6th subplot
axes[5].set_visible(False)

plt.suptitle('Performance Divergence Across Regions in Top 5 Candidate Surveys', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('/work/survey_divergence.png', dpi=150)
print("Figure saved to /work/survey_divergence.png")

# Now let's look at the overall response-level analysis
# Create a visualization showing the distribution of values by language
fig2, ax = plt.subplots(figsize=(12, 6))
result = db.query("""
    SELECT user_language, value
    FROM qualtrics__response
""")
df = db.frame(result)

# Create boxplot
bp = df.boxplot(column='value', by='user_language', ax=ax, 
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

# Compute the key statistics for the report
print("\n\n=== KEY STATISTICS FOR REPORT ===")
print(f"Total responses: {len(df)}")
print(f"Overall score: {df['value'].mean()*10:.2f}")
print(f"Top market segment (value > 7) score: {df[df['value']>7]['value'].mean()*10:.2f}")
print(f"Low market segment (value < 3) score: {df[df['value']<3]['value'].mean()*10:.2f}")
print(f"Top market segment size: {len(df[df['value']>7])} ({len(df[df['value']>7])/len(df)*100:.1f}%)")
print(f"Low market segment size: {len(df[df['value']<3])} ({len(df[df['value']<3])/len(df)*100:.1f}%)")

# Market concentration
print(f"\nTop 3 regions by score: FR (55.38), ZH (55.02), NL (54.99)")
print(f"Bottom 3 regions by score: ES (54.41), EN (54.79), JA (54.82)")
print(f"Max-min spread: {df.groupby('user_language')['value'].mean().max()*10 - df.groupby('user_language')['value'].mean().min()*10:.2f}")

# Survey-level analysis
print(f"\nMost divergent survey (SUR10001791916):")
print(f"  PT: 8.83 (score 88.3)")
print(f"  ES: 7.85 (score 78.5)")
print(f"  DE: 4.33 (score 43.3)")
print(f"  JA: 1.59 (score 15.9)")
print(f"  Spread: 7.24")
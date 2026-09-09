import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load all response data
result = db.query("""
    SELECT value, user_language, contact_language, survey_id, survey_response_id,
           question_type, response_text
    FROM qualtrics__response
""")
df = db.frame(result)
print(f"Total responses: {len(df)}")

# Overall performance score (avg value * 10)
overall_score = df['value'].mean() * 10
print(f"Overall performance score: {overall_score:.2f}")

# Performance by region (user_language)
lang_perf = df.groupby('user_language').agg(
    n_responses=('value', 'count'),
    mean_value=('value', 'mean'),
    std_value=('value', 'std'),
    min_value=('value', 'min'),
    max_value=('value', 'max')
).reset_index()
lang_perf['score'] = lang_perf['mean_value'] * 10
lang_perf = lang_perf.sort_values('score', ascending=False)
print("\nPerformance by region (user_language):")
print(lang_perf.to_string(index=False))

# Check if any region has avg > 7 or < 3
print(f"\nRegions with mean_value > 7: {len(lang_perf[lang_perf['mean_value'] > 7])}")
print(f"Regions with mean_value < 3: {len(lang_perf[lang_perf['mean_value'] < 3])}")

# Since no region meets the threshold at aggregate level, 
# let's analyze at the response level: markets with revenue > $7 (value > 7)
# vs markets with revenue < $3 (value < 3)

# Top markets: responses with value > 7
top_market = df[df['value'] > 7]
low_market = df[df['value'] < 3]
mid_market = df[(df['value'] >= 3) & (df['value'] <= 7)]

print(f"\nTop markets (value > 7): {len(top_market)} responses")
print(f"Low markets (value < 3): {len(low_market)} responses")
print(f"Mid markets (3-7): {len(mid_market)} responses")

# Performance in top vs low markets
print(f"\nTop markets - avg score: {top_market['value'].mean()*10:.2f}")
print(f"Low markets - avg score: {low_market['value'].mean()*10:.2f}")
print(f"Performance gap: {top_market['value'].mean()*10 - low_market['value'].mean()*10:.2f}")

# But wait, the task says "revenue exceeding $7" - this might mean the average value per market
# Let me also check: what if "revenue" is the average value of a market?
# Then top markets would be those with avg > 7... but none exist globally

# Let me instead look at the distribution of high-value responses by language
print("\n\nHigh-value responses (value > 7) by language:")
hv_by_lang = top_market.groupby('user_language').agg(
    n_high=('value', 'count'),
    pct_high=('value', lambda x: len(x)/len(df[df['user_language']==x.iloc[0]])*100 if len(df[df['user_language']==x.iloc[0]])>0 else 0)
).reset_index()
print(hv_by_lang.to_string(index=False))

print("\n\nLow-value responses (value < 3) by language:")
lv_by_lang = low_market.groupby('user_language').agg(
    n_low=('value', 'count')
).reset_index()
print(lv_by_lang.to_string(index=False))

# Let me compute the percentage of high-value responses per language
lang_pcts = []
for lang in df['user_language'].unique():
    lang_df = df[df['user_language'] == lang]
    total = len(lang_df)
    high = len(lang_df[lang_df['value'] > 7])
    low = len(lang_df[lang_df['value'] < 3])
    lang_pcts.append({
        'language': lang,
        'total': total,
        'n_high': high,
        'pct_high': high/total*100,
        'n_low': low,
        'pct_low': low/total*100,
        'avg_score': lang_df['value'].mean()*10
    })
lang_pct_df = pd.DataFrame(lang_pcts)
lang_pct_df = lang_pct_df.sort_values('avg_score', ascending=False)
print("\n\nLanguage market analysis:")
print(lang_pct_df.to_string(index=False))

# Create visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Average score by language
ax1 = axes[0]
colors = ['#2ecc71' if v > 55 else '#e74c3c' if v < 54 else '#f39c12' for v in lang_pct_df['avg_score']]
bars = ax1.bar(lang_pct_df['language'], lang_pct_df['avg_score'], color=colors)
ax1.axhline(y=overall_score, color='gray', linestyle='--', label=f'Overall: {overall_score:.1f}')
ax1.set_xlabel('Region (Language)')
ax1.set_ylabel('Performance Score (avg × 10)')
ax1.set_title('Performance Score by Region')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Percentage of high-value responses by language
ax2 = axes[1]
colors2 = ['#2ecc71' if v > 30 else '#e74c3c' if v < 29 else '#f39c12' for v in lang_pct_df['pct_high']]
ax2.bar(lang_pct_df['language'], lang_pct_df['pct_high'], color=colors2)
ax2.set_xlabel('Region (Language)')
ax2.set_ylabel('% of Responses with Value > 7')
ax2.set_title('High-Revenue Market Segment by Region')
ax2.tick_params(axis='x', rotation=45)

# Plot 3: Percentage of low-value responses by language
ax3 = axes[2]
colors3 = ['#e74c3c' if v > 30 else '#2ecc71' if v < 28 else '#f39c12' for v in lang_pct_df['pct_low']]
ax3.bar(lang_pct_df['language'], lang_pct_df['pct_low'], color=colors3)
ax3.set_xlabel('Region (Language)')
ax3.set_ylabel('% of Responses with Value < 3')
ax3.set_title('Low-Revenue Market Segment by Region')
ax3.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/performance_divergence.png', dpi=150)
print("\nFigure saved to /work/performance_divergence.png")

# Now let's also look at the survey level to find the most divergent survey
# which might be the "photoeditor" app
result2 = db.query("""
    SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 2
""")
df2 = db.frame(result2)

# Find survey with max divergence
survey_stats = df2.groupby('survey_id').agg(
    n_langs=('n', 'count'),
    total_resp=('n', 'sum'),
    max_avg=('avg_v', 'max'),
    min_avg=('avg_v', 'min')
).reset_index()
survey_stats['spread'] = survey_stats['max_avg'] - survey_stats['min_avg']
survey_stats['max_lang'] = df2.groupby('survey_id').apply(lambda x: x.loc[x['avg_v'].idxmax(), 'user_language'])
survey_stats['min_lang'] = df2.groupby('survey_id').apply(lambda x: x.loc[x['avg_v'].idxmin(), 'user_language'])

# Top 5 divergent surveys with >=3 languages
top5 = survey_stats[survey_stats['n_langs'] >= 3].sort_values('spread', ascending=False).head(5)
print("\n\nTop 5 most divergent surveys (potential photoeditor app):")
for _, row in top5.iterrows():
    print(f"Survey: {row['survey_id']}, Spread: {row['spread']:.2f}, "
          f"Langs: {row['n_langs']}, Total: {row['total_resp']}")

# Get details of the most divergent survey
top_sid = top5.iloc[0]['survey_id']
print(f"\n\nDetailed language breakdown for most divergent survey ({top_sid}):")
lang_details = df2[df2['survey_id'] == top_sid].sort_values('avg_v', ascending=False)
print(lang_details.to_string(index=False))

# Get survey name
result3 = db.query(f"SELECT survey_name, project_category, project_type FROM qualtrics__survey WHERE survey_id = '{top_sid}' LIMIT 1")
survey_info = db.frame(result3)
print(f"\nSurvey info: {survey_info.to_string(index=False)}")

# The overall score for this survey
result4 = db.query(f"SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = '{top_sid}'")
overall = db.frame(result4)
print(f"Survey overall score: {overall['avg_val'].iloc[0]*10:.2f} (n={overall['n'].iloc[0]})")
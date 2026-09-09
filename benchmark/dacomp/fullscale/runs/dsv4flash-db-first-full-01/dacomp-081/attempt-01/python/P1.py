import pandas as pd
import numpy as np
import json

# Load all response data
rows = []
with open('/results/S5.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))
# 72000 rows - let's use db.query with a more efficient approach
# Actually, let's query the response data aggregated by survey and language
result = db.query("""
    SELECT survey_id, user_language, COUNT(*) AS n, 
           AVG(value) AS avg_v, MIN(value) AS min_v, MAX(value) AS max_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 3
""")
df = db.frame(result)
print(f"Rows: {len(df)}")
print(df.head(10))
print(f"Surveys: {df['survey_id'].nunique()}")
print(f"Languages: {df['user_language'].nunique()}")

# For each survey, compute max and min language avg
survey_stats = df.groupby('survey_id').agg(
    n_langs=('n', 'count'),
    total_resp=('n', 'sum'),
    max_lang_avg=('avg_v', 'max'),
    min_lang_avg=('avg_v', 'min'),
    max_lang=('avg_v', lambda x: x.idxmax()),
    min_lang=('avg_v', lambda x: x.idxmin())
).reset_index()

survey_stats['spread'] = survey_stats['max_lang_avg'] - survey_stats['min_lang_avg']

# Find surveys with high divergence (max > 7, min < 3) and at least 3 languages
divergent = survey_stats[
    (survey_stats['max_lang_avg'] > 7.0) & 
    (survey_stats['min_lang_avg'] < 3.0) & 
    (survey_stats['n_langs'] >= 3)
].sort_values('spread', ascending=False)

print(f"\nDivergent surveys (max>7, min<3, >=3 langs): {len(divergent)}")
print(divergent.head(10).to_string())

# Look at the top divergent survey
top_survey = divergent.iloc[0]['survey_id']
print(f"\n\nTop survey: {top_survey}")
print(f"Spread: {divergent.iloc[0]['spread']:.2f}")

# Get language details for top survey
lang_details = df[df['survey_id'] == top_survey].sort_values('avg_v', ascending=False)
print(lang_details.to_string())
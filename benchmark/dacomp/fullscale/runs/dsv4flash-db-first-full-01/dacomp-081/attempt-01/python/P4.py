import pandas as pd
import numpy as np

# Per-survey and per-language stats
result = db.query("""
    SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 2
""")
df = db.frame(result)

# Survey-level stats
survey_stats = df.groupby('survey_id').agg(
    n_langs=('n', 'count'),
    total_resp=('n', 'sum'),
    overall_avg=('avg_v', lambda x: np.average(x, weights=df.loc[x.index, 'n'])),
    max_lang_avg=('avg_v', 'max'),
    min_lang_avg=('avg_v', 'min')
).reset_index()
survey_stats['overall_score'] = survey_stats['overall_avg'] * 10
survey_stats['spread'] = survey_stats['max_lang_avg'] - survey_stats['min_lang_avg']

# Look for surveys with overall score around 72 (7.0-7.4) and spread >= 4 with at least 3 langs
candidates = survey_stats[
    (survey_stats['overall_score'].between(65, 80)) &
    (survey_stats['n_langs'] >= 3) &
    (survey_stats['spread'] >= 3)
].sort_values('spread', ascending=False)
print("Candidates with overall score 65-80, >=3 langs, spread>=3:")
print(candidates.head(20).to_string())

# Also find surveys with overall score close to 85 (8.3-8.7)
cand85 = survey_stats[
    (survey_stats['overall_score'].between(80, 90)) &
    (survey_stats['n_langs'] >= 3)
].sort_values('overall_score', ascending=False)
print("\n\nSurveys with overall score 80-90, >=3 langs:")
print(cand85.head(20).to_string())

# Find surveys that have a language with avg > 8 AND overall around 7.2
match = survey_stats[
    (survey_stats['max_lang_avg'] > 8.0) &
    (survey_stats['overall_avg'].between(6.5, 7.8)) &
    (survey_stats['n_langs'] >= 3)
].sort_values('overall_avg')
print("\n\nSurveys with a language avg>8 AND overall avg 6.5-7.8:")
print(match.head(20).to_string())
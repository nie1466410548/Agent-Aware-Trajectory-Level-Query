import pandas as pd
import numpy as np
import json

# Load the full subset of 660 profiles from archived results
df = pd.read_json('/results/S15.rows.jsonl', lines=True)
print("Rows:", len(df))
print(df.dtypes)
print(df.head(3))

# Percentiles
for col in ['job_health_score', 'avg_career_development_score', 'talent_saturation', 'talent_quality_index', 'avg_weekly_hours']:
    print(col, df[col].quantile([0.10, 0.25, 0.50, 0.75, 0.90]).round(3).to_dict())

print("\nHealth Q1:", df['job_health_score'].quantile(0.25))
print("Dev Q1:", df['avg_career_development_score'].quantile(0.25))

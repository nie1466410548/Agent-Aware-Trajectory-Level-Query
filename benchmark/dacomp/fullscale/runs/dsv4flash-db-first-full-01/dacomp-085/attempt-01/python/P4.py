import pandas as pd, numpy as np, json

rows = []
with open('/results/S15.rows.jsonl') as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

cols = ['job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
        'job_health_score', 'avg_career_development_score', 'retention_difficulty_level',
        'is_work_shift_required', 'avg_weekly_hours', 'current_employees_count',
        'active_positions_count', 'talent_saturation', 'talent_quality_index']

df = pd.DataFrame(rows, columns=cols)

# === PERCENTILES ===
print("=== Percentiles ===")
for col in ['job_health_score', 'avg_career_development_score', 'talent_saturation', 'talent_quality_index', 'avg_weekly_hours']:
    q = df[col].quantile([0.10, 0.25, 0.50, 0.75, 0.90]).round(4)
    print(f"\n{col}:")
    print(q.to_dict())

# === COMPOSITE OUTPUT INDEX ===
# Normalize health score (0-100) and dev score (1-5) to 0-1 and average
df['health_norm'] = df['job_health_score'] / 100.0
df['dev_norm'] = df['avg_career_development_score'] / 5.0
df['output_index'] = 0.5 * df['health_norm'] + 0.5 * df['dev_norm']

# === COMPOSITE INPUT INDEX ===
# Normalize saturation (0-~2) and weekly hours (35-55) to 0-1
sat_max = df['talent_saturation'].max()
sat_min = df['talent_saturation'].min()
hrs_max = df['avg_weekly_hours'].max()
hrs_min = df['avg_weekly_hours'].min()
df['sat_norm'] = (df['talent_saturation'] - sat_min) / (sat_max - sat_min)
df['hrs_norm'] = (df['avg_weekly_hours'] - hrs_min) / (hrs_max - hrs_min)
# Higher input = more staffing/effort invested
df['input_index'] = 0.5 * df['sat_norm'] + 0.5 * df['hrs_norm']

# Input-to-output ratio (higher = more input per unit output)
df['io_ratio'] = df['input_index'] / (df['output_index'] + 0.01)  # avoid division by zero

print("\n=== Output Index ===")
print(df['output_index'].describe())
print("\n=== Input Index ===")
print(df['input_index'].describe())
print("\n=== IO Ratio ===")
print(df['io_ratio'].describe())

# === MISMATCH DEFINITION ===
# Mismatch: High/Very High competition but LOW output (bottom quartile of output_index)
# AND/OR health/dev below their respective medians
low_output_threshold = df['output_index'].quantile(0.25)
low_health_threshold = df['job_health_score'].quantile(0.25)
low_dev_threshold = df['avg_career_development_score'].quantile(0.25)
high_io_threshold = df['io_ratio'].quantile(0.75)

print(f"\n=== Thresholds ===")
print(f"Low output threshold (Q1): {low_output_threshold:.4f}")
print(f"Low health threshold (Q1): {low_health_threshold:.2f}")
print(f"Low dev threshold (Q1): {low_dev_threshold:.2f}")
print(f"High IO ratio (Q3): {high_io_threshold:.4f}")

# Mismatch = output <= Q1 (bottom quartile)
df['is_mismatch'] = df['output_index'] <= low_output_threshold
# Imbalanced = IO ratio >= Q3 (top quartile)  
df['is_imbalanced'] = df['io_ratio'] >= high_io_threshold

# Both conditions
df['is_mismatch_and_imbalanced'] = df['is_mismatch'] & df['is_imbalanced']

print(f"\nMismatch count: {df['is_mismatch'].sum()}")
print(f"Imbalanced count: {df['is_imbalanced'].sum()}")
print(f"Both: {df['is_mismatch_and_imbalanced'].sum()}")

# Save key data
df.to_csv('/work/analysis_data.csv', index=False)
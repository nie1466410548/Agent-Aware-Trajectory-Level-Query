import pandas as pd, numpy as np, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Reload
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

# Compute indices
df['health_norm'] = df['job_health_score'] / 100.0
df['dev_norm'] = df['avg_career_development_score'] / 5.0
df['output_index'] = 0.5 * df['health_norm'] + 0.5 * df['dev_norm']
sat_max, sat_min = df['talent_saturation'].max(), df['talent_saturation'].min()
hrs_max, hrs_min = df['avg_weekly_hours'].max(), df['avg_weekly_hours'].min()
df['sat_norm'] = (df['talent_saturation'] - sat_min) / (sat_max - sat_min)
df['hrs_norm'] = (df['avg_weekly_hours'] - hrs_min) / (hrs_max - hrs_min)
df['input_index'] = 0.5 * df['sat_norm'] + 0.5 * df['hrs_norm']
df['io_ratio'] = df['input_index'] / (df['output_index'] + 0.01)

low_output_threshold = df['output_index'].quantile(0.25)
high_io_threshold = df['io_ratio'].quantile(0.75)
df['is_mismatch'] = df['output_index'] <= low_output_threshold
df['is_imbalanced'] = df['io_ratio'] >= high_io_threshold

# === ANALYSIS BY WORK CHARACTERISTICS ===
print("=== Mismatch Profiles by Retention Difficulty ===")
print(df[df['is_mismatch']]['retention_difficulty_level'].value_counts())
print("\n=== Non-Mismatch Profiles by Retention Difficulty ===")
print(df[~df['is_mismatch']]['retention_difficulty_level'].value_counts())

print("\n=== Mismatch Profiles by Shift Required ===")
print(df[df['is_mismatch']]['is_work_shift_required'].value_counts())
print("\n=== Non-Mismatch Profiles by Shift Required ===")
print(df[~df['is_mismatch']]['is_work_shift_required'].value_counts())

print("\n=== Mismatch Profiles Avg Weekly Hours ===")
print(df[df['is_mismatch']]['avg_weekly_hours'].describe())
print("\n=== Non-Mismatch Profiles Avg Weekly Hours ===")
print(df[~df['is_mismatch']]['avg_weekly_hours'].describe())

# === Cross-tabulations ===
print("\n=== Cross-tab: Mismatch × Retention Difficulty ===")
ct = pd.crosstab(df['is_mismatch'], df['retention_difficulty_level'], margins=True)
print(ct)

print("\n=== Cross-tab: Mismatch × Shift Required ===")
ct2 = pd.crosstab(df['is_mismatch'], df['is_work_shift_required'], margins=True)
print(ct2)

# === Imbalanced profiles ===
print("\n=== Imbalanced Profiles by Retention Difficulty ===")
print(df[df['is_imbalanced']]['retention_difficulty_level'].value_counts())

print("\n=== Imbalanced Profiles by Shift Required ===")
print(df[df['is_imbalanced']]['is_work_shift_required'].value_counts())

# === Both conditions ===
both = df[df['is_mismatch'] & df['is_imbalanced']]
print(f"\n=== Both Mismatch AND Imbalanced: {len(both)} profiles ===")
print(both[['job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
            'job_health_score', 'avg_career_development_score', 'talent_saturation',
            'talent_quality_index', 'retention_difficulty_level', 'avg_weekly_hours']].head(20))

# Save both
both.to_csv('/work/both_mismatch_imbalanced.csv', index=False)
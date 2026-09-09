import pandas as pd, numpy as np, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

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
df['health_norm'] = df['job_health_score'] / 100.0
df['dev_norm'] = df['avg_career_development_score'] / 5.0
df['output_index'] = 0.5 * df['health_norm'] + 0.5 * df['dev_norm']
sat_max, sat_min = df['talent_saturation'].max(), df['talent_saturation'].min()
hrs_max, hrs_min = df['avg_weekly_hours'].max(), df['avg_weekly_hours'].min()
df['sat_norm'] = (df['talent_saturation'] - sat_min) / (sat_max - sat_min)
df['hrs_norm'] = (df['avg_weekly_hours'] - hrs_min) / (hrs_max - hrs_min)
df['input_index'] = 0.5 * df['sat_norm'] + 0.5 * df['hrs_norm']
df['io_ratio'] = df['input_index'] / (df['output_index'] + 0.01)
df['is_mismatch'] = df['output_index'] <= df['output_index'].quantile(0.25)
df['is_imbalanced'] = df['io_ratio'] >= df['io_ratio'].quantile(0.75)

# === Statistical tests ===
mis = df[df['is_mismatch']]
nomis = df[~df['is_mismatch']]

# Weekly hours t-test
t_stat, p_val = stats.ttest_ind(mis['avg_weekly_hours'], nomis['avg_weekly_hours'])
print(f"Weekly hours t-test: t={t_stat:.3f}, p={p_val:.4f}")

# Chi-square: retention difficulty
ct = pd.crosstab(df['is_mismatch'], df['retention_difficulty_level'])
chi2, p_chi, dof, _ = stats.chi2_contingency(ct)
print(f"Retention difficulty chi2: chi2={chi2:.3f}, p={p_chi:.4f}")

# Chi-square: shift required
ct2 = pd.crosstab(df['is_mismatch'], df['is_work_shift_required'])
chi2_2, p_chi2, _, _ = stats.chi2_contingency(ct2)
print(f"Shift required chi2: chi2={chi2_2:.3f}, p={p_chi2:.4f}")

# Correlation analysis
corr_cols = ['talent_saturation', 'talent_quality_index', 'job_health_score', 'avg_career_development_score', 'avg_weekly_hours']
print("\n=== Correlation Matrix ===")
print(df[corr_cols].corr().round(3))

# === PRIORITY RANKING ===
# Build priority score for critical (mismatch AND imbalanced) profiles
critical = df[df['is_mismatch'] & df['is_imbalanced']].copy()

# Components:
# 1. Output deficit (reverse of output_index): higher = worse output
critical['output_deficit'] = 1 - critical['output_index']
# 2. Input waste (io_ratio): higher = more input per output
# 3. Competition severity
crit_map = {'Very High': 2, 'High': 1}
critical['competition_severity'] = critical['talent_competition_level'].map(crit_map)
# 4. Retention difficulty
ret_map = {'Very High': 3, 'High': 2, 'Medium': 1, 'Low': 0}
critical['retention_severity'] = critical['retention_difficulty_level'].map(ret_map)

# Normalize components to 0-1
critical['output_deficit_n'] = (critical['output_deficit'] - critical['output_deficit'].min()) / (critical['output_deficit'].max() - critical['output_deficit'].min())
critical['io_n'] = (critical['io_ratio'] - critical['io_ratio'].min()) / (critical['io_ratio'].max() - critical['io_ratio'].min())
critical['comp_n'] = critical['competition_severity'] / 2.0
critical['ret_n'] = critical['retention_severity'] / 3.0

# Priority score (weighted)
critical['priority_score'] = (0.35*critical['output_deficit_n'] + 0.25*critical['io_n'] +
                              0.20*critical['comp_n'] + 0.20*critical['ret_n'])

critical = critical.sort_values('priority_score', ascending=False).reset_index(drop=True)
critical['priority_rank'] = range(1, len(critical)+1)

print(f"\n=== PRIORITY RANKING (Top 30 of {len(critical)}) ===")
print(critical[['priority_rank', 'job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
                'job_health_score', 'avg_career_development_score', 'talent_saturation',
                'io_ratio', 'priority_score']].head(30).to_string())

critical.to_csv('/work/priority_ranking.csv', index=False)

# === Job title family analysis of critical profiles ===
print("\n=== Critical Profiles by Job Title (top 15) ===")
print(critical['job_title'].value_counts().head(15).to_string())

print("\n=== Critical Profiles by Value Tier ===")
print(critical['job_value_tier'].value_counts().to_string())

print("\n=== Critical Profiles by Competition ===")
print(critical['talent_competition_level'].value_counts().to_string())

print("\n=== Critical Profiles by Retention Difficulty ===")
print(critical['retention_difficulty_level'].value_counts().to_string())
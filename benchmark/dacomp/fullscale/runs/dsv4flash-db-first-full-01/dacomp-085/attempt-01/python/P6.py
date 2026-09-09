import pandas as pd, numpy as np, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Reload data
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

# ========== FIGURE 1: Scatter plot of Output vs Input ==========
plt.figure(figsize=(12, 8))
colors = df['is_mismatch'].map({True: 'red', False: 'steelblue'})
plt.scatter(df['input_index'], df['output_index'], c=colors, alpha=0.6, s=40)
plt.axhline(y=low_output_threshold, color='red', linestyle='--', alpha=0.5, label=f'Low Output Threshold (Q1={low_output_threshold:.3f})')
plt.axvline(x=df['input_index'].median(), color='gray', linestyle=':', alpha=0.5, label='Median Input')
plt.xlabel('Input Index (Staffing Effort)', fontsize=12)
plt.ylabel('Output Index (Performance)', fontsize=12)
plt.title('Job Profiles: Output vs Input (High/Very High Competition)', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('/work/fig1_output_vs_input.png', dpi=150)
plt.close()

# ========== FIGURE 2: Bar chart of retention difficulty by mismatch ==========
plt.figure(figsize=(10, 6))
ct = pd.crosstab(df['is_mismatch'], df['retention_difficulty_level'], normalize='index')
ct.plot(kind='bar', ax=plt.gca(), colormap='viridis')
plt.xlabel('Mismatch Status (False=No Mismatch, True=Mismatch)', fontsize=12)
plt.ylabel('Proportion', fontsize=12)
plt.title('Retention Difficulty Distribution by Mismatch Status', fontsize=14)
plt.legend(title='Retention Difficulty')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('/work/fig2_retention_by_mismatch.png', dpi=150)
plt.close()

# ========== FIGURE 3: Weekly hours distribution ==========
plt.figure(figsize=(10, 6))
df[df['is_mismatch']]['avg_weekly_hours'].hist(alpha=0.6, label='Mismatch', bins=20, color='red')
df[~df['is_mismatch']]['avg_weekly_hours'].hist(alpha=0.4, label='No Mismatch', bins=20, color='steelblue')
plt.xlabel('Average Weekly Hours', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Weekly Hours Distribution: Mismatch vs Non-Mismatch', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('/work/fig3_weekly_hours.png', dpi=150)
plt.close()

# ========== FIGURE 4: Top 20 worst-off profiles ==========
worst = df[df['is_mismatch']].sort_values('output_index').head(20)
plt.figure(figsize=(12, 8))
x = np.arange(len(worst))
width = 0.35
plt.bar(x - width/2, worst['job_health_score'], width, label='Health Score', color='coral')
plt.bar(x + width/2, worst['avg_career_development_score']*20, width, label='Dev Score (×20)', color='lightblue')
plt.axhline(y=df['job_health_score'].median(), color='coral', linestyle='--', alpha=0.5, label=f'Median Health={df["job_health_score"].median():.1f}')
plt.xlabel('Job Profile', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.title('Bottom 20 Mismatch Profiles: Health and Development Scores', fontsize=14)
plt.xticks(x, [f"{r['job_title'][:15]}..." for _, r in worst.iterrows()], rotation=45, ha='right', fontsize=8)
plt.legend()
plt.tight_layout()
plt.savefig('/work/fig4_bottom20.png', dpi=150)
plt.close()

print("Figures saved successfully")
print(f"Total mismatch profiles: {df['is_mismatch'].sum()}")
print(f"Total imbalanced: {df['is_imbalanced'].sum()}")
print(f"Both: {(df['is_mismatch'] & df['is_imbalanced']).sum()}")

# Get the 79 critical profiles sorted
critical = df[df['is_mismatch'] & df['is_imbalanced']].sort_values(['output_index', 'io_ratio'], ascending=[True, False])
print("\n=== Top 20 Critical Profiles (Mismatch AND Imbalanced) ===")
print(critical[['job_profile_id', 'job_title', 'job_value_tier', 'talent_competition_level',
                 'job_health_score', 'avg_career_development_score', 'talent_saturation',
                 'talent_quality_index', 'retention_difficulty_level', 'avg_weekly_hours',
                 'output_index', 'io_ratio']].head(20).to_string())

critical.to_csv('/work/critical_profiles.csv', index=False)
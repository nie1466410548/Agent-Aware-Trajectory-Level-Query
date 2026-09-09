import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define columns
columns = ['Job Title', 'Work Experience Requirement', 'Foreign Language Requirement',
           'Gender Requirement', 'Company Type', 'Industry', 'Work Location',
           'Working Hours', 'Benefits', 'Salary Range', 'salary_min', 'salary_max']

# Load data from result file
rows = []
with open('/results/S36.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=columns)
print(f"Total records: {len(df)}")
print(df[['salary_min', 'salary_max']].describe())

# Compute midpoint salary
df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2.0
print(f"\nSalary midpoint stats:")
print(df['salary_mid'].describe())

# Filter out extreme outliers
df_clean = df[(df['salary_min'] >= 1000) & (df['salary_max'] <= 50000) & (df['salary_mid'] >= 1000)]
print(f"\nAfter filtering outliers: {len(df_clean)} records")

# Salary distribution - histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_clean['salary_mid'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Monthly Salary Midpoint (yuan)', fontsize=12)
axes[0].set_ylabel('Number of Job Postings', fontsize=12)
axes[0].set_title('Distribution of Starting Salaries\nfor Vocational School Graduates', fontsize=13)
axes[0].axvline(df_clean['salary_mid'].mean(), color='red', linestyle='--', label=f'Mean: {df_clean["salary_mid"].mean():.0f}')
axes[0].axvline(df_clean['salary_mid'].median(), color='green', linestyle='--', label=f'Median: {df_clean["salary_mid"].median():.0f}')
axes[0].legend()

axes[1].boxplot([df_clean['salary_min'], df_clean['salary_max']], labels=['Salary Min', 'Salary Max'])
axes[1].set_ylabel('Monthly Salary (yuan)', fontsize=12)
axes[1].set_title('Salary Range Distribution', fontsize=13)

plt.tight_layout()
plt.savefig('/work/salary_distribution.png', dpi=150)
plt.close()
print("Saved salary_distribution.png")

# Benefits distribution
benefits_map = {
    'Five social insurances': 'Five Social Insurances',
    'Housing provident fund': 'Housing Provident Fund',
    'Commercial insurance': 'Commercial Insurance',
    'Paid annual leave': 'Paid Annual Leave',
    'Double pay at the end': 'Double Pay at Year End',
    'Performance bonus': 'Performance Bonus',
    'Year-end bonus': 'Year-End Bonus',
    'Meal allowance': 'Meal Allowance',
    'Accommodation': 'Housing/Accommodation',
    'Meals provided': 'Meals Provided',
    'Overtime pay': 'Overtime Pay',
    'Holiday benefits': 'Holiday Benefits',
    'training': 'Professional Training',
    'travel': 'Employee Travel',
    'Communication allowance': 'Communication Allowance',
    'Full attendance bonus': 'Full Attendance Bonus',
    'High-temperature allowance': 'High-Temp Allowance',
    'shuttle': 'Free Shuttle Bus',
    'medical checkup': 'Medical Checkups',
    'Work uniform': 'Work Uniform',
    'Flexible working hours': 'Flexible Hours'
}

benefits_data = df_clean['Benefits'].fillna('')

benefit_counts = {}
for keyword, label in benefits_map.items():
    count = benefits_data.str.contains(keyword, case=False, na=False).sum()
    benefit_counts[label] = count

benefit_series = pd.Series(benefit_counts).sort_values(ascending=False)
print("\nBenefits Distribution:")
print(benefit_series)

# Benefits chart
fig, ax = plt.subplots(figsize=(12, 8))
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(benefit_series)))
bars = ax.barh(range(len(benefit_series)), benefit_series.values, color=colors[::-1])
ax.set_yticks(range(len(benefit_series)))
ax.set_yticklabels(benefit_series.index, fontsize=10)
ax.set_xlabel('Number of Job Postings', fontsize=12)
ax.set_title('Benefits Distribution for Vocational School Graduates', fontsize=14)
for i, (v, pct) in enumerate(zip(benefit_series.values, (benefit_series.values / len(df_clean) * 100))):
    ax.text(v + 20, i, f'{v} ({pct:.1f}%)', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/benefits_distribution.png', dpi=150)
plt.close()
print("Saved benefits_distribution.png")

# Analyze which qualities affect salary
# 1. Work Experience
print("\n\n=== SALARY BY WORK EXPERIENCE ===")
exp_agg = df_clean.groupby('Work Experience Requirement').agg(
    count=('salary_mid', 'count'),
    mean_salary=('salary_mid', 'mean'),
    median_salary=('salary_mid', 'median')
).sort_values('mean_salary', ascending=False)
print(exp_agg[exp_agg['count'] >= 5].to_string())

# 2. Foreign Language
print("\n\n=== SALARY BY FOREIGN LANGUAGE ===")
lang_agg = df_clean.groupby('Foreign Language Requirement').agg(
    count=('salary_mid', 'count'),
    mean_salary=('salary_mid', 'mean')
).sort_values('mean_salary', ascending=False)
print(lang_agg[lang_agg['count'] >= 5].to_string())

# 3. Gender
print("\n\n=== SALARY BY GENDER ===")
gender_agg = df_clean.groupby('Gender Requirement').agg(
    count=('salary_mid', 'count'),
    mean_salary=('salary_mid', 'mean')
)
print(gender_agg.to_string())

# 4. Company Type
print("\n\n=== SALARY BY COMPANY TYPE ===")
co_agg = df_clean.groupby('Company Type').agg(
    count=('salary_mid', 'count'),
    mean_salary=('salary_mid', 'mean')
).sort_values('mean_salary', ascending=False)
print(co_agg[co_agg['count'] >= 5].to_string())

# 5. Industry
print("\n\n=== SALARY BY INDUSTRY ===")
ind_agg = df_clean.groupby('Industry').agg(
    count=('salary_mid', 'count'),
    mean_salary=('salary_mid', 'mean')
).sort_values('mean_salary', ascending=False)
print(ind_agg[ind_agg['count'] >= 10].head(20).to_string())

# Create visualization for main factors affecting salary
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Work Experience
exp_simple_map = {
    'No limit': 'No experience limit',
    'Fresh graduates': 'Fresh graduates',
    'More than one year of work experience': '1+ year',
    'Two years or more of work experience': '2+ years',
    'Three years or more of work experience': '3+ years',
    'Four years or more of work experience': '4+ years',
    'Five years or more of work experience': '5+ years',
    'Six years or more of work experience': '6+ years',
    'Eight years or more of work experience': '8+ years',
    'Ten years or more of work experience': '10+ years',
}
exp_plot = exp_agg[exp_agg.index.isin(exp_simple_map.keys())].copy()
exp_plot.index = [exp_simple_map[i] for i in exp_plot.index]
exp_plot = exp_plot.sort_values('mean_salary')

colors_exp = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(exp_plot)))
axes[0,0].barh(range(len(exp_plot)), exp_plot['mean_salary'].values, color=colors_exp)
axes[0,0].set_yticks(range(len(exp_plot)))
axes[0,0].set_yticklabels(exp_plot.index, fontsize=9)
axes[0,0].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[0,0].set_title('A: Work Experience Requirement', fontsize=12)
for i, v in enumerate(exp_plot['mean_salary'].values):
    axes[0,0].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# 2. Company Type
co_plot = co_agg[co_agg['count'] >= 5].sort_values('mean_salary')
colors_co = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(co_plot)))
axes[0,1].barh(range(len(co_plot)), co_plot['mean_salary'].values, color=colors_co)
axes[0,1].set_yticks(range(len(co_plot)))
axes[0,1].set_yticklabels(co_plot.index, fontsize=9)
axes[0,1].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[0,1].set_title('B: Company Type', fontsize=12)
for i, v in enumerate(co_plot['mean_salary'].values):
    axes[0,1].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# 3. Industry top 15
ind_plot = ind_agg[ind_agg['count'] >= 20].sort_values('mean_salary').tail(15)
colors_ind = plt.cm.viridis(np.linspace(0.1, 0.9, len(ind_plot)))
axes[1,0].barh(range(len(ind_plot)), ind_plot['mean_salary'].values, color=colors_ind)
axes[1,0].set_yticks(range(len(ind_plot)))
axes[1,0].set_yticklabels([x[:35] for x in ind_plot.index], fontsize=8)
axes[1,0].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[1,0].set_title('C: Industry', fontsize=12)
for i, v in enumerate(ind_plot['mean_salary'].values):
    axes[1,0].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# 4. Foreign Language
lang_plot = lang_agg[lang_agg['count'] >= 5].sort_values('mean_salary')
colors_lang = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(lang_plot)))
axes[1,1].barh(range(len(lang_plot)), lang_plot['mean_salary'].values, color=colors_lang)
axes[1,1].set_yticks(range(len(lang_plot)))
axes[1,1].set_yticklabels([str(x)[:40] for x in lang_plot.index], fontsize=9)
axes[1,1].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[1,1].set_title('D: Foreign Language Requirement', fontsize=12)
for i, v in enumerate(lang_plot['mean_salary'].values):
    axes[1,1].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('/work/salary_factors.png', dpi=150)
plt.close()
print("Saved salary_factors.png")

# Salary difference by benefit presence
print("\n\n=== SALARY DIFFERENCE BY BENEFIT PRESENCE ===")
benefit_salary_diff = {}
for keyword, label in benefits_map.items():
    has_benefit = df_clean['Benefits'].fillna('').str.contains(keyword, case=False, na=False)
    if has_benefit.sum() >= 30:
        mean_with = df_clean.loc[has_benefit, 'salary_mid'].mean()
        mean_without = df_clean.loc[~has_benefit, 'salary_mid'].mean()
        diff = mean_with - mean_without
        benefit_salary_diff[label] = (mean_with, mean_without, diff, has_benefit.sum())
        print(f"{label:30s}: With={mean_with:7.0f}, Without={mean_without:7.0f}, Diff={diff:+.0f} (n={has_benefit.sum()})")

# Create benefit salary impact chart
benefit_diff_df = pd.DataFrame(benefit_salary_diff).T
benefit_diff_df.columns = ['with', 'without', 'diff', 'count']
benefit_diff_df = benefit_diff_df.sort_values('diff', ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
colors = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(benefit_diff_df)))
bars = ax.barh(range(len(benefit_diff_df)), benefit_diff_df['diff'].values, color=colors)
ax.set_yticks(range(len(benefit_diff_df)))
ax.set_yticklabels(benefit_diff_df.index, fontsize=9)
ax.set_xlabel('Salary Difference (yuan/month) - Jobs with vs without benefit', fontsize=11)
ax.set_title('Impact of Benefits on Starting Salary', fontsize=14)
ax.axvline(0, color='black', linestyle='-', linewidth=0.5)
for i, v in enumerate(benefit_diff_df['diff'].values):
    ax.text(v + 20 if v >= 0 else v - 50, i, f'{v:+.0f}', va='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/benefit_salary_impact.png', dpi=150)
plt.close()
print("Saved benefit_salary_impact.png")

print("\n\nDone! All analysis complete.")
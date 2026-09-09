import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

columns = ['Job Title', 'Work Experience Requirement', 'Foreign Language Requirement',
           'Gender Requirement', 'Company Type', 'Industry', 'Work Location',
           'Working Hours', 'Benefits', 'Salary Range', 'salary_min', 'salary_max']

rows = []
with open('/results/S36.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=columns)
df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2.0
df_clean = df[(df['salary_min'] >= 1000) & (df['salary_max'] <= 50000) & (df['salary_mid'] >= 1000)]
print(f"After filtering outliers: {len(df_clean)} records")
print(f"Salary midpoint stats:\n{df_clean['salary_mid'].describe()}")

# Salary distribution - histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_clean['salary_mid'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Monthly Salary Midpoint (yuan)', fontsize=12)
axes[0].set_ylabel('Number of Job Postings', fontsize=12)
axes[0].set_title('Distribution of Starting Salaries\nfor Vocational School Graduates', fontsize=13)
axes[0].axvline(df_clean['salary_mid'].mean(), color='red', linestyle='--', label=f'Mean: {df_clean["salary_mid"].mean():.0f}')
axes[0].axvline(df_clean['salary_mid'].median(), color='green', linestyle='--', label=f'Median: {df_clean["salary_mid"].median():.0f}')
axes[0].legend()

bp = axes[1].boxplot([df_clean['salary_min'], df_clean['salary_max']], tick_labels=['Salary Min', 'Salary Max'])
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

print("\n\nIntermediate complete - saving factor chart next")
df_clean.to_csv('/work/vocational_clean.csv', index=False)
print("Saved /work/vocational_clean.csv")
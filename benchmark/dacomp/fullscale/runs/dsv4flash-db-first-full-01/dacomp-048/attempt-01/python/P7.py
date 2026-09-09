import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

df_clean = pd.read_csv('/work/vocational_clean.csv')
print(f"Loaded {len(df_clean)} records")

# Salary by Work Experience
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

exp_agg = df_clean.groupby('Work Experience Requirement')['salary_mid'].agg(['count', 'mean', 'median'])
exp_plot = exp_agg[exp_agg.index.isin(exp_simple_map.keys())].copy()
exp_plot.index = [exp_simple_map[i] for i in exp_plot.index]
exp_plot = exp_plot.sort_values('mean')

# Statistical test: ANOVA across experience groups
exp_data = [df_clean.loc[df_clean['Work Experience Requirement'] == k, 'salary_mid'].values 
            for k in exp_simple_map.keys() if df_clean.loc[df_clean['Work Experience Requirement'] == k, 'salary_mid'].count() >= 5]
f_stat, p_val = stats.f_oneway(*exp_data)
print(f"\nANOVA - Work Experience groups: F={f_stat:.2f}, p={p_val:.2e}")

# t-test: Fresh graduates vs No limit
fresh = df_clean.loc[df_clean['Work Experience Requirement'] == 'Fresh graduates', 'salary_mid']
nolimit = df_clean.loc[df_clean['Work Experience Requirement'] == 'No limit', 'salary_mid']
t, p = stats.ttest_ind(fresh, nolimit, equal_var=False)
print(f"t-test Fresh grads vs No-limit: t={t:.2f}, p={p:.4f}")

# t-test: 2+years vs No limit
two = df_clean.loc[df_clean['Work Experience Requirement'] == 'Two years or more of work experience', 'salary_mid']
t, p = stats.ttest_ind(two, nolimit, equal_var=False)
print(f"t-test 2+years vs No-limit: t={t:.2f}, p={p:.4f}")

t, p = stats.ttest_ind(df_clean.loc[df_clean['Work Experience Requirement'] == 'Five years or more of work experience', 'salary_mid'], nolimit, equal_var=False)
print(f"t-test 5+years vs No-limit: t={t:.2f}, p={p:.4f}")

# Foreign Language analysis
df_clean['has_english'] = df_clean['Foreign Language Requirement'].fillna('').str.contains('English', case=False, na=False)
with_en = df_clean.loc[df_clean['has_english'], 'salary_mid']
without_en = df_clean.loc[~df_clean['has_english'], 'salary_mid']
t, p = stats.ttest_ind(with_en, without_en, equal_var=False)
print(f"\nEnglish requirement: n_with={len(with_en)}, mean_with={with_en.mean():.0f}, n_without={len(without_en)}, mean_without={without_en.mean():.0f}")
print(f"t-test English vs no English: t={t:.2f}, p={p:.4f}")

# Gender analysis
male = df_clean.loc[df_clean['Gender Requirement'] == 'male', 'salary_mid']
female = df_clean.loc[df_clean['Gender Requirement'] == 'female', 'salary_mid']
none_g = df_clean.loc[df_clean['Gender Requirement'] == 'none', 'salary_mid']
t, p = stats.ttest_ind(female, male, equal_var=False)
print(f"\nGender: female mean={female.mean():.0f} (n={len(female)}), male mean={male.mean():.0f} (n={len(male)}), none mean={none_g.mean():.0f} (n={len(none_g)})")
print(f"t-test female vs male: t={t:.2f}, p={p:.4f}")

# Company type analysis - ANOVA
co_types = ['Listed companies', 'Private joint-stock companies', 'Private companies', 'Taiwanese/Hong Kong capital', 'State-owned enterprises']
co_data = [df_clean.loc[df_clean['Company Type'] == ct, 'salary_mid'].values for ct in co_types if df_clean.loc[df_clean['Company Type'] == ct, 'salary_mid'].count() >= 10]
f_stat, p_val = stats.f_oneway(*co_data)
print(f"\nANOVA - Company Type groups: F={f_stat:.2f}, p={p_val:.2e}")

# listed vs private
listed = df_clean.loc[df_clean['Company Type'] == 'Listed companies', 'salary_mid']
private = df_clean.loc[df_clean['Company Type'] == 'Private companies', 'salary_mid']
t, p = stats.ttest_ind(listed, private, equal_var=False)
print(f"t-test Listed vs Private: t={t:.2f}, p={p:.4f}")

# Benefit salary impact
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
    'Work uniform': 'Work Uniform',
    'Flexible working hours': 'Flexible Hours'
}

benefit_salary_diff = {}
for keyword, label in benefits_map.items():
    has_benefit = df_clean['Benefits'].fillna('').str.contains(keyword, case=False, na=False)
    if has_benefit.sum() >= 50:
        mean_with = df_clean.loc[has_benefit, 'salary_mid'].mean()
        mean_without = df_clean.loc[~has_benefit, 'salary_mid'].mean()
        diff = mean_with - mean_without
        n = has_benefit.sum()
        t, p = stats.ttest_ind(df_clean.loc[has_benefit, 'salary_mid'], df_clean.loc[~has_benefit, 'salary_mid'], equal_var=False)
        benefit_salary_diff[label] = (mean_with, mean_without, diff, n, p)
        print(f"{label:30s}: With={mean_with:7.0f}, Without={mean_without:7.0f}, Diff={diff:+.0f} (n={n}, p={p:.4f})")

benefit_diff_df = pd.DataFrame(benefit_salary_diff).T
benefit_diff_df.columns = ['with', 'without', 'diff', 'count', 'pval']
benefit_diff_df = benefit_diff_df.sort_values('diff', ascending=True)

# Create factor comparison chart
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# A: Work Experience
colors_exp = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(exp_plot)))
axes[0,0].barh(range(len(exp_plot)), exp_plot['mean'].values, color=colors_exp)
axes[0,0].set_yticks(range(len(exp_plot)))
axes[0,0].set_yticklabels(exp_plot.index, fontsize=9)
axes[0,0].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[0,0].set_title('A: Work Experience Requirement', fontsize=12)
for i, v in enumerate(exp_plot['mean'].values):
    axes[0,0].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# B: Company Type
co_agg = df_clean.groupby('Company Type')['salary_mid'].agg(['count', 'mean'])
co_plot = co_agg[co_agg['count'] >= 10].sort_values('mean')
colors_co = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(co_plot)))
axes[0,1].barh(range(len(co_plot)), co_plot['mean'].values, color=colors_co)
axes[0,1].set_yticks(range(len(co_plot)))
axes[0,1].set_yticklabels(co_plot.index, fontsize=9)
axes[0,1].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[0,1].set_title('B: Company Type', fontsize=12)
for i, v in enumerate(co_plot['mean'].values):
    axes[0,1].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# C: Industry top 15 (single-tag industries preferred)
# Use the first industry tag for simplicity
df_clean['primary_industry'] = df_clean['Industry'].fillna('Other').str.split(',').str[0].str.strip()
ind_agg = df_clean.groupby('primary_industry')['salary_mid'].agg(['count', 'mean'])
ind_plot = ind_agg[ind_agg['count'] >= 20].sort_values('mean').tail(15)
colors_ind = plt.cm.viridis(np.linspace(0.1, 0.9, len(ind_plot)))
axes[1,0].barh(range(len(ind_plot)), ind_plot['mean'].values, color=colors_ind)
axes[1,0].set_yticks(range(len(ind_plot)))
axes[1,0].set_yticklabels([x[:35] for x in ind_plot.index], fontsize=8)
axes[1,0].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[1,0].set_title('C: Industry (Primary Tag)', fontsize=12)
for i, v in enumerate(ind_plot['mean'].values):
    axes[1,0].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

# D: Foreign Language
lang_agg = df_clean.groupby('Foreign Language Requirement')['salary_mid'].agg(['count', 'mean'])
lang_plot = lang_agg[lang_agg['count'] >= 5].sort_values('mean')
colors_lang = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(lang_plot)))
axes[1,1].barh(range(len(lang_plot)), lang_plot['mean'].values, color=colors_lang)
axes[1,1].set_yticks(range(len(lang_plot)))
axes[1,1].set_yticklabels([str(x)[:40] for x in lang_plot.index], fontsize=9)
axes[1,1].set_xlabel('Average Monthly Salary (yuan)', fontsize=11)
axes[1,1].set_title('D: Foreign Language Requirement', fontsize=12)
for i, v in enumerate(lang_plot['mean'].values):
    axes[1,1].text(v + 50, i, f'{v:.0f}', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('/work/salary_factors.png', dpi=150)
plt.close()
print("Saved salary_factors.png")

# Benefit impact chart
fig, ax = plt.subplots(figsize=(12, 8))
colors = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(benefit_diff_df)))
bars = ax.barh(range(len(benefit_diff_df)), benefit_diff_df['diff'].values, color=colors)
ax.set_yticks(range(len(benefit_diff_df)))
ax.set_yticklabels(benefit_diff_df.index, fontsize=9)
ax.set_xlabel('Salary Difference (yuan/month): Jobs with vs without benefit', fontsize=11)
ax.set_title('How Benefit Offerings Relate to Starting Salary', fontsize=14)
ax.axvline(0, color='black', linestyle='-', linewidth=0.5)
for i, v in enumerate(benefit_diff_df['diff'].values):
    ax.text(v + 20 if v >= 0 else v - 60, i, f'{v:+.0f}', va='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/benefit_salary_impact.png', dpi=150)
plt.close()
print("Saved benefit_salary_impact.png")

# Also check Working Hours impact - correlation
def parse_hours(h):
    if pd.isna(h):
        return None
    import re
    m = re.search(r'(\d+\.?\d*)\s*hours/day', str(h))
    return float(m.group(1)) if m else None

df_clean['hours_day'] = df_clean['Working Hours'].apply(parse_hours)
hours_agg = df_clean.groupby('hours_day')['salary_mid'].agg(['count', 'mean'])
print("\n\n=== SALARY BY HOURS PER DAY ===")
print(hours_agg[hours_agg['count'] >= 20].to_string())

# Working days per week
def parse_days(h):
    if pd.isna(h):
        return None
    import re
    m = re.search(r'(\d+\.?\d*)\s*days/week', str(h))
    return float(m.group(1)) if m else None

df_clean['days_week'] = df_clean['Working Hours'].apply(parse_days)
days_agg = df_clean.groupby('days_week')['salary_mid'].agg(['count', 'mean'])
print("\n=== SALARY BY DAYS PER WEEK ===")
print(days_agg[days_agg['count'] >= 20].to_string())

# Work location
loc_agg = df_clean.groupby('Work Location')['salary_mid'].agg(['count', 'mean'])
print("\n\n=== SALARY BY WORK LOCATION (top 12) ===")
print(loc_agg[loc_agg['count'] >= 50].sort_values('mean', ascending=False).head(12).to_string())

print("\nAll complete")
import pandas as pd
import numpy as np
from scipy import stats

df_clean = pd.read_csv('/work/vocational_clean.csv')
print(f"Loaded {len(df_clean)} records")

# Salary bands distribution
bands = [(0, 3000, '<3,000'), (3000, 4000, '3,000-4,000'), (4000, 5000, '4,000-5,000'),
         (5000, 6000, '5,000-6,000'), (6000, 7000, '6,000-7,000'), (7000, 8000, '7,000-8,000'),
         (8000, 10000, '8,000-10,000'), (10000, 15000, '10,000-15,000'), (15000, 1e9, '>15,000')]

print("\n=== SALARY BAND DISTRIBUTION (midpoint) ===")
for lo, hi, label in bands:
    cnt = ((df_clean['salary_mid'] >= lo) & (df_clean['salary_mid'] < hi)).sum()
    print(f"{label:20s}: {cnt:5d}  ({cnt/len(df_clean)*100:.1f}%)")

# Percentiles
print("\n=== SALARY PERCENTILES ===")
for pct in [5, 10, 25, 50, 75, 90, 95]:
    print(f"P{pct}: {np.percentile(df_clean['salary_mid'], pct):.0f} yuan")

# Min/Max distribution
print("\n=== SALARY MIN DISTRIBUTION ===")
for lo, hi, label in bands:
    cnt = ((df_clean['salary_min'] >= lo) & (df_clean['salary_min'] < hi)).sum()
    print(f"{label:20s}: {cnt:5d}  ({cnt/len(df_clean)*100:.1f}%)")

# English proficiency - targeted comparison
prof_en = df_clean['Foreign Language Requirement'].fillna('').str.contains('Proficiency in English', case=False, na=False)
others = df_clean['Foreign Language Requirement'].fillna('').str.contains('Proficiency in English', case=False, na=False)
en_prof_group = df_clean[prof_en]['salary_mid']
rest_group = df_clean[~prof_en]['salary_mid']
t, p = stats.ttest_ind(en_prof_group, rest_group, equal_var=False)
print(f"\n'Proficiency in English required' group: n={len(en_prof_group)}, mean={en_prof_group.mean():.0f}, median={en_prof_group.median():.0f}")
print(f"All others: n={len(rest_group)}, mean={rest_group.mean():.0f}")
print(f"t-test: t={t:.2f}, p={p:.4f}")

# Any English mention
any_en = df_clean['Foreign Language Requirement'].fillna('').str.contains('English', case=False, na=False)
print(f"\nAny English mention: n={any_en.sum()}, mean={df_clean[any_en]['salary_mid'].mean():.0f}")
print(f"No English: n={(~any_en).sum()}, mean={df_clean[~any_en]['salary_mid'].mean():.0f}")

# Ordinal experience -> salary correlation
exp_order = {
    'Fresh graduates': 0,
    'More than one year of work experience': 1,
    'No limit': 1,
    'Two years or more of work experience': 2,
    'Three years or more of work experience': 3,
    'Four years or more of work experience': 4,
    'Five years or more of work experience': 5,
    'Six years or more of work experience': 6,
    'Eight years or more of work experience': 8,
    'Ten years or more of work experience': 10,
}
df_clean['exp_years'] = df_clean['Work Experience Requirement'].map(exp_order)
valid = df_clean.dropna(subset=['exp_years'])
# Exclude 'No limit' from correlation since it's ambiguous
corr_valid = valid[valid['Work Experience Requirement'] != 'No limit']
r, p = stats.pearsonr(corr_valid['exp_years'], corr_valid['salary_mid'])
print(f"\nPearson corr(experience years, salary midpoint) [excluding No-limit]: r={r:.3f}, p={p:.2e}")
print(f"n={len(corr_valid)}")

# Spearman
rho, sp = stats.spearmanr(corr_valid['exp_years'], corr_valid['salary_mid'])
print(f"Spearman corr: rho={rho:.3f}, p={sp:.2e}")

# Top job titles for vocational graduates
print("\n=== TOP 20 JOB TITLES ===")
top_jobs = df_clean['Job Title'].value_counts().head(20)
print(top_jobs.to_string())

# Check job titles of high-paying roles (>=8000 midpoint)
high_pay = df_clean[df_clean['salary_mid'] >= 8000]
print(f"\nHigh-pay jobs (>=8000): {len(high_pay)} ({len(high_pay)/len(df_clean)*100:.1f}%)")
print("Top job titles among high-pay:")
print(high_pay['Job Title'].value_counts().head(15).to_string())

print("\nDone")
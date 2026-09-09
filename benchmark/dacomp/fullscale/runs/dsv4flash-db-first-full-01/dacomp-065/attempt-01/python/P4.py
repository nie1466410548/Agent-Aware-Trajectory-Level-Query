import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, ttest_ind

# ============ 1. Company premium across score dimensions ============
# Load application-level scores with controls
data = db.frame(db.query("""
WITH cat AS (
  SELECT application_id, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  WHERE i.technical_score IS NOT NULL
  GROUP BY i.application_id
)
SELECT * FROM app_agg
"""))

edu_map = {'Bootcamp Certificate': 0, 'Bachelor': 1, 'Master': 2, 'MBA': 2, 'PhD': 3}
tier_map = {'other': 0, 'tier3': 1, 'tier2': 2, 'tier1': 3, 'international': 1}
data['edu_num'] = data['education_level'].map(edu_map)
data['tier_num'] = data['university_tier'].map(tier_map)
data['is_faang'] = (data['company_cat'] == 'FAANG').astype(float)
data['is_major_tech'] = (data['company_cat'] == 'Major_Tech').astype(float)

score_cols = ['avg_tech', 'avg_ps', 'avg_comm', 'avg_cf', 'avg_lead']
dim_names = ['Technical', 'Problem Solving', 'Communication', 'Culture Fit', 'Leadership']

print("=== FAANG premium (coefficient) on each score dimension, with controls ===")
print("Model: score ~ FAANG + Major_Tech + edu + yoe + skills + univ_tier\n")

results = []
for score_col, dim in zip(score_cols, dim_names):
    m = data.dropna(subset=[score_col, 'edu_num', 'years_of_experience', 'skill_count', 'tier_num'])
    X = np.column_stack([
        np.ones(m.shape[0]), m['is_faang'].values, m['is_major_tech'].values,
        m['edu_num'].values, m['years_of_experience'].values,
        m['skill_count'].values, m['tier_num'].values
    ])
    y = m[score_col].values
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    n, k = X.shape
    y_pred = X @ beta
    mse = np.sum((y - y_pred)**2) / (n - k)
    var_beta = mse * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(var_beta))
    t = beta / se
    p = 2 * (1 - stats.t.cdf(np.abs(t), n - k))
    results.append({'dimension': dim, 'faang_coef': beta[1], 'faang_se': se[1], 'faang_t': t[1], 'faang_p': p[1],
                    'major_coef': beta[2], 'major_se': se[2], 'major_t': t[2], 'major_p': p[2], 'n': n})
    print(f"{dim:<18} FAANG coef={beta[1]:.4f} (SE={se[1]:.4f}, t={t[1]:.2f}, p={p[1]:.4f})  MajorTech coef={beta[2]:.4f} (p={p[2]:.4f})")

res_df = pd.DataFrame(results)

# ============ 2. Bias regression: demographics on technical score ============
# Load interview-level data with company category and demographics
int_data = db.frame(db.query("""
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT DISTINCT i.application_id, i.interview_id, i.interviewer_user_id,
       i.technical_score, i.candidate_gender, i.candidate_race,
       i.interviewer_gender, i.interviewer_level,
       cat.company_cat
FROM greenhouse__interview_enhanced i
JOIN cat ON cat.application_id = i.application_id
WHERE i.technical_score IS NOT NULL
"""))

# Filter to non-null candidate gender and interviewer gender, Male/Female only for interaction test
subset = int_data.dropna(subset=['candidate_gender', 'interviewer_gender']).copy()
subset = subset[subset['candidate_gender'].isin(['Male', 'Female'])]
subset = subset[subset['interviewer_gender'].isin(['Male', 'Female'])]

print(f"\n=== Gender interaction sample: {subset.shape[0]} interviews ===")

# Dummies
subset['cand_male'] = (subset['candidate_gender'] == 'Male').astype(float)
subset['int_male'] = (subset['interviewer_gender'] == 'Male').astype(float)
subset['cand_x_int'] = subset['cand_male'] * subset['int_male']

X = np.column_stack([
    np.ones(subset.shape[0]),
    subset['cand_male'].values,
    subset['int_male'].values,
    subset['cand_x_int'].values
])
y = subset['technical_score'].values
beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
n, k = X.shape
y_pred = X @ beta
mse = np.sum((y - y_pred)**2) / (n - k)
var_beta = mse * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(var_beta))
t = beta / se
p = 2 * (1 - stats.t.cdf(np.abs(t), n - k))

print("=== OLS: technical_score ~ cand_male + int_male + cand_male*int_male ===")
print(f"{'Variable':<20} {'Coef':<10} {'SE':<10} {'t':<10} {'p':<10}")
for i, name in enumerate(['Intercept (F cand, F int)', 'Candidate Male', 'Interviewer Male', 'Male-Male Interaction']):
    print(f"{name:<20} {beta[i]:<10.4f} {se[i]:<10.4f} {t[i]:<10.4f} {p[i]:<10.6f}")

# ============ 3. Company background + demographics together ============
print("\n=== OLS: technical_score ~ company + gender + race (with controls) ===")
bias_data = db.frame(db.query("""
WITH cat AS (
  SELECT DISTINCT a.application_id, a.education_level, a.years_of_experience, a.skill_count, a.university_tier,
    CASE
      WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat,
    a.candidate_gender, a.candidate_race
  FROM greenhouse__application_enhanced a
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         cat.candidate_gender, cat.candidate_race,
         AVG(i.technical_score) AS avg_tech
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
"""))

bias_data['edu_num'] = bias_data['education_level'].map(edu_map)
bias_data['tier_num'] = bias_data['university_tier'].map(tier_map)
bias_data['is_faang'] = (bias_data['company_cat'] == 'FAANG').astype(float)
bias_data['is_major_tech'] = (bias_data['company_cat'] == 'Major_Tech').astype(float)

# Restrict to candidates with known race (most complete demographic)
race_subset = bias_data.dropna(subset=['avg_tech', 'edu_num', 'candidate_race'])
print(f"Sample with race info: {race_subset.shape[0]}")

race_map = {'Asian': 0, 'White': 1, 'Black': 2, 'Hispanic': 3, 'Native American': 4, 'Other': 5}
race_subset['race_num'] = race_subset['candidate_race'].map(race_map)

# Model: tech ~ company + race + edu + yoe + skills
m = race_subset.dropna(subset=['race_num'])
X = np.column_stack([
    np.ones(m.shape[0]), m['is_faang'].values, m['is_major_tech'].values,
    m['race_num'].values, m['edu_num'].values,
    m['years_of_experience'].values, m['skill_count'].values, m['tier_num'].values
])
y = m['avg_tech'].values
beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
n, k = X.shape
y_pred = X @ beta
mse = np.sum((y - y_pred)**2) / (n - k)
var_beta = mse * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(var_beta))
t = beta / se
p = 2 * (1 - stats.t.cdf(np.abs(t), n - k))

print(f"{'Variable':<20} {'Coef':<10} {'SE':<10} {'t':<10} {'p':<10}")
names = ['Intercept', 'FAANG', 'Major_Tech', 'Race', 'Education', 'Years Exp', 'Skills', 'Univ Tier']
for i in range(k):
    print(f"{names[i]:<20} {beta[i]:<10.4f} {se[i]:<10.4f} {t[i]:<10.4f} {p[i]:<10.6f}")

# ============ 4. Hiring funnel by company category ============
print("\n=== Hiring funnel by company category (distinct applications) ===")
funnel = db.frame(db.query("""
WITH cat AS (
  SELECT DISTINCT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
  COUNT(*) AS n_apps,
  SUM(CASE WHEN a.stage_application_review=1 THEN 1 ELSE 0 END) AS app_review,
  SUM(CASE WHEN a.stage_phone_screen=1 THEN 1 ELSE 0 END) AS phone_screen,
  SUM(CASE WHEN a.stage_technical_interview=1 THEN 1 ELSE 0 END) AS tech_int,
  SUM(CASE WHEN a.stage_panel_interview=1 THEN 1 ELSE 0 END) AS panel,
  SUM(CASE WHEN a.stage_final_interview=1 THEN 1 ELSE 0 END) AS final_int,
  SUM(CASE WHEN a.stage_offer=1 THEN 1 ELSE 0 END) AS offer,
  SUM(CASE WHEN a.stage_hired=1 THEN 1 ELSE 0 END) AS hired
FROM (SELECT DISTINCT application_id, stage_application_review, stage_phone_screen, stage_technical_interview,
      stage_panel_interview, stage_final_interview, stage_offer, stage_hired
      FROM greenhouse__application_enhanced) a
JOIN cat ON cat.application_id = a.application_id
GROUP BY cat.company_cat
ORDER BY hired DESC
"""))
print(funnel)

# Convert to rates
funnel_rates = funnel.copy()
for col in ['app_review', 'phone_screen', 'tech_int', 'panel', 'final_int', 'offer', 'hired']:
    funnel_rates[col + '_rate'] = funnel_rates[col] / funnel_rates['n_apps']
print("\n=== Funnel rates ===")
print(funnel_rates[['company_cat', 'app_review_rate', 'phone_screen_rate', 'tech_int_rate', 'panel_rate', 'final_int_rate', 'offer_rate', 'hired_rate']])

# ============ 5. Visualizations ============
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: FAANG premium by dimension
ax = axes[0]
x_pos = np.arange(len(res_df))
ax.bar(x_pos, res_df['faang_coef'].values, yerr=res_df['faang_se'].values*1.96, capsize=5, color='#440154')
ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(res_df['dimension'], rotation=15)
ax.set_ylabel('FAANG coefficient (controlled)')
ax.set_title('FAANG Premium by Score Dimension')
for i, p in enumerate(res_df['faang_p']):
    ax.text(x_pos[i], res_df['faang_coef'].values[i]+0.05, f"p={p:.3f}", ha='center', fontsize=8)

# Plot 2: Funnel rates
ax = axes[1]
funnel_rates.set_index('company_cat').T[['FAANG', 'Major_Tech', 'Traditional']].plot(
    kind='line', marker='o', ax=ax)
ax.set_xticks(range(7))
ax.set_xticklabels(['App Review', 'Phone', 'Tech Int', 'Panel', 'Final', 'Offer', 'Hired'], rotation=30)
ax.set_ylabel('Proportion of applicants reaching stage')
ax.set_title('Hiring Funnel by Company Background')
ax.legend(title='Company')

# Plot 3: Gender interaction
ax = axes[2]
groups = ['F-F', 'F-M', 'M-F', 'M-M']
means = [7.506, 7.499, 7.522, 7.717]
ax.bar(groups, means, color=['#21918c', '#3b528b', '#440154', '#fde725'])
ax.set_ylabel('Mean Technical Score')
ax.set_title('Mean Score by Candidate-Interviewer Gender Pairing')
for i, v in enumerate(means):
    ax.text(i, v+0.03, f'{v:.2f}', ha='center')

plt.tight_layout()
plt.savefig('/work/bias_quantification.png', dpi=120)
plt.close()

print("\nAll regression and bias analyses complete.")
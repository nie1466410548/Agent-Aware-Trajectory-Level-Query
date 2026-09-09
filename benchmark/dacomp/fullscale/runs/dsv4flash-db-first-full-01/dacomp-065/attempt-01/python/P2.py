import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data with controls
reg_data = db.frame(db.query("""
WITH cat AS (
  SELECT application_id, candidate_company, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         cat.education_level,
         cat.years_of_experience,
         cat.skill_count,
         cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
"""))

print(f"Data shape: {reg_data.shape}")
print(f"Missing values:\n{reg_data.isnull().sum()}")

# Check education_level values
print(f"\nEducation levels: {reg_data['education_level'].unique()}")
print(f"University tiers: {reg_data['university_tier'].unique()}")

# Create dummy variables for regression
# Education: ordered
edu_map = {'Bootcamp Certificate': 0, 'Bachelor': 1, 'Master': 2, 'MBA': 2, 'PhD': 3}
reg_data['edu_num'] = reg_data['education_level'].map(edu_map)

# University tier
tier_map = {'other': 0, 'tier3': 1, 'tier2': 2, 'tier1': 3, 'international': 1}
reg_data['tier_num'] = reg_data['university_tier'].map(tier_map)

# Company category dummies
reg_data['is_faang'] = (reg_data['company_cat'] == 'FAANG').astype(float)
reg_data['is_major_tech'] = (reg_data['company_cat'] == 'Major_Tech').astype(float)
reg_data['is_traditional'] = (reg_data['company_cat'] == 'Traditional').astype(float)

# Drop rows with missing values
model_data = reg_data.dropna(subset=['avg_tech', 'edu_num', 'years_of_experience', 'skill_count', 'tier_num'])
print(f"Model data shape after dropping NAs: {model_data.shape}")

# ===== Model 1: Company category only =====
X1 = np.column_stack([
    np.ones(model_data.shape[0]),
    model_data['is_faang'].values,
    model_data['is_major_tech'].values
])
y = model_data['avg_tech'].values

beta1, residuals1, rank1, s1 = np.linalg.lstsq(X1, y, rcond=None)
n1, k1 = X1.shape
y_pred1 = X1 @ beta1
mse1 = np.sum((y - y_pred1)**2) / (n1 - k1)
var_beta1 = mse1 * np.linalg.inv(X1.T @ X1)
se1 = np.sqrt(np.diag(var_beta1))
t1 = beta1 / se1
p1 = 2 * (1 - stats.t.cdf(np.abs(t1), n1 - k1))
r2_1 = 1 - np.sum((y - y_pred1)**2) / np.sum((y - np.mean(y))**2)

print("\n=== Model 1: Company Category Only ===")
print(f"R-squared: {r2_1:.4f}")
print(f"{'Variable':<20} {'Coef':<10} {'Std.Err':<10} {'t':<10} {'p-value':<10}")
print("-"*60)
print(f"{'Intercept (Traditional)':<20} {beta1[0]:<10.4f} {se1[0]:<10.4f} {t1[0]:<10.4f} {p1[0]:<10.6f}")
print(f"{'FAANG':<20} {beta1[1]:<10.4f} {se1[1]:<10.4f} {t1[1]:<10.4f} {p1[1]:<10.6f}")
print(f"{'Major_Tech':<20} {beta1[2]:<10.4f} {se1[2]:<10.4f} {t1[2]:<10.4f} {p1[2]:<10.6f}")

# ===== Model 2: Company category + education + experience + skills =====
X2 = np.column_stack([
    np.ones(model_data.shape[0]),
    model_data['is_faang'].values,
    model_data['is_major_tech'].values,
    model_data['edu_num'].values,
    model_data['years_of_experience'].values,
    model_data['skill_count'].values,
    model_data['tier_num'].values
])

beta2, residuals2, rank2, s2 = np.linalg.lstsq(X2, y, rcond=None)
n2, k2 = X2.shape
y_pred2 = X2 @ beta2
mse2 = np.sum((y - y_pred2)**2) / (n2 - k2)
var_beta2 = mse2 * np.linalg.inv(X2.T @ X2)
se2 = np.sqrt(np.diag(var_beta2))
t2 = beta2 / se2
p2 = 2 * (1 - stats.t.cdf(np.abs(t2), n2 - k2))
r2_2 = 1 - np.sum((y - y_pred2)**2) / np.sum((y - np.mean(y))**2)

print("\n=== Model 2: With Controls (Education, Experience, Skills, University Tier) ===")
print(f"R-squared: {r2_2:.4f}")
print(f"{'Variable':<25} {'Coef':<10} {'Std.Err':<10} {'t':<10} {'p-value':<10}")
print("-"*65)
vars2 = ['Intercept (Traditional)', 'FAANG', 'Major_Tech', 'Education_Level', 'Years_Experience', 'Skill_Count', 'Univ_Tier']
for i in range(k2):
    print(f"{vars2[i]:<25} {beta2[i]:<10.4f} {se2[i]:<10.4f} {t2[i]:<10.4f} {p2[i]:<10.6f}")

# ===== Model 3: Test if FAANG coefficient shrinks significantly =====
print(f"\nFAANG coefficient change: Model1={beta1[1]:.4f}, Model2={beta2[1]:.4f}")
print(f"Major_Tech coefficient change: Model1={beta1[2]:.4f}, Model2={beta2[2]:.4f}")

# ===== Additional analysis: Hiring outcome (logistic regression approximation) =====
# Let's look at offer stage reach rate
print("\n=== Hiring Outcome Analysis ===")
hiring_data = db.frame(db.query("""
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(*) AS n_apps,
       SUM(a.stage_offer) AS reached_offer,
       SUM(a.stage_hired) AS hired,
       AVG(CAST(a.stage_offer AS FLOAT)) AS offer_rate,
       AVG(CAST(a.stage_hired AS FLOAT)) AS hire_rate
FROM greenhouse__application_enhanced a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_technical_interview = 1
GROUP BY cat.company_cat
ORDER BY offer_rate DESC
"""))
print(hiring_data)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Technical score by company category
sns.boxplot(x='company_cat', y='avg_tech', data=model_data, 
            order=['FAANG', 'Major_Tech', 'Traditional'], hue='company_cat',
            palette='viridis', legend=False, ax=axes[0])
axes[0].set_title('Technical Score by Company Background', fontsize=13)
axes[0].set_xlabel('Company Category')
axes[0].set_ylabel('Average Technical Score')

# Plot 2: Positive recommendation rate
rec_rate = model_data.groupby('company_cat')['ever_pos_rec'].mean()
colors = ['#440154', '#21918c', '#fde725']
axes[1].bar(['FAANG', 'Major_Tech', 'Traditional'], rec_rate.values, color=colors)
axes[1].set_title('Positive Recommendation Rate by Company Background', fontsize=13)
axes[1].set_xlabel('Company Category')
axes[1].set_ylabel('Positive Recommendation Rate')
axes[1].set_ylim(0, 1)

plt.tight_layout()
plt.savefig('/work/company_effects.png', dpi=120)
plt.close()

print("\nRegression analysis complete.")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, kruskal, ttest_ind, chi2_contingency

# ========== 1. BIAS BY CANDIDATE DEMOGRAPHICS ==========
# Load deduplicated application-level data with demographics
bias_app_data = db.frame(db.query("""
SELECT DISTINCT a.application_id, a.candidate_gender, a.candidate_race, 
       a.candidate_disability_status, a.candidate_veteran_status,
       a.stage_offer, a.stage_hired, a.status
FROM greenhouse__application_enhanced a
"""))

print("=== Application Demographics ===")
print(bias_app_data['candidate_gender'].value_counts(dropna=False))
print(bias_app_data['candidate_race'].value_counts(dropna=False))
print(bias_app_data['candidate_disability_status'].value_counts(dropna=False))
print(bias_app_data['candidate_veteran_status'].value_counts(dropna=False))

# Gender and hiring
gender_hiring = pd.crosstab(bias_app_data['candidate_gender'], bias_app_data['stage_hired'])
print("\n=== Gender × Hired ===")
print(gender_hiring)
if gender_hiring.shape[0] > 1 and gender_hiring.shape[1] > 1:
    chi2, p, dof, exp = chi2_contingency(gender_hiring)
    print(f"Chi-square: {chi2:.4f}, p-value: {p:.6f}")

# Race and hiring
race_hiring = pd.crosstab(bias_app_data['candidate_race'], bias_app_data['stage_hired'])
print("\n=== Race × Hired ===")
print(race_hiring)
if race_hiring.shape[0] > 1 and race_hiring.shape[1] > 1:
    chi2, p, dof, exp = chi2_contingency(race_hiring)
    print(f"Chi-square: {chi2:.4f}, p-value: {p:.6f}")

# ========== 2. INTERVIEW-LEVEL BIAS ANALYSIS ==========
# Load distinct interview scores with demographics
bias_int_data = db.frame(db.query("""
SELECT DISTINCT i.application_id, i.interview_id, i.interviewer_user_id,
       i.technical_score, i.problem_solving_score, i.communication_score,
       i.culture_fit_score, i.leadership_score, i.overall_recommendation,
       i.candidate_gender, i.candidate_race, i.candidate_disability_status, i.candidate_veteran_status,
       i.interviewer_gender, i.interviewer_level, i.interviewer_experience_years,
       i.interview_time_of_day, i.interview_day_of_week, i.interview_season,
       i.interview_duration_minutes, i.interviewer_is_hiring_manager,
       i.follow_up_questions_count, i.interviewer_satisfaction
FROM greenhouse__interview_enhanced i
WHERE i.technical_score IS NOT NULL
"""))

print(f"\nInterview-level data shape: {bias_int_data.shape}")
print(f"Unique interviews: {bias_int_data['interview_id'].nunique()}")

# Check interviewer demographics
print("\n=== Interviewer Gender ===")
print(bias_int_data['interviewer_gender'].value_counts(dropna=False))

print("\n=== Interviewer Level ===")
print(bias_int_data['interviewer_level'].value_counts(dropna=False))

# ===== BIAS: Candidate gender vs technical score =====
print("\n=== Technical Score by Candidate Gender ===")
for gender in bias_int_data['candidate_gender'].dropna().unique():
    subset = bias_int_data[bias_int_data['candidate_gender'] == gender]['technical_score']
    print(f"{gender}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

# ANOVA
gender_groups = [bias_int_data[bias_int_data['candidate_gender'] == g]['technical_score'].values 
                 for g in bias_int_data['candidate_gender'].dropna().unique()]
if len(gender_groups) >= 2:
    f, p = f_oneway(*gender_groups)
    print(f"ANOVA by candidate gender: F={f:.4f}, p={p:.6f}")

# ===== BIAS: Candidate race vs technical score =====
print("\n=== Technical Score by Candidate Race ===")
for race in bias_int_data['candidate_race'].dropna().unique():
    subset = bias_int_data[bias_int_data['candidate_race'] == race]['technical_score']
    print(f"{race}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

race_groups = [bias_int_data[bias_int_data['candidate_race'] == r]['technical_score'].values 
               for r in bias_int_data['candidate_race'].dropna().unique()]
if len(race_groups) >= 2:
    f, p = f_oneway(*race_groups)
    print(f"ANOVA by candidate race: F={f:.4f}, p={p:.6f}")
    # Non-parametric
    h, p_kw = kruskal(*race_groups)
    print(f"Kruskal-Wallis by candidate race: H={h:.4f}, p={p_kw:.6f}")

# ===== BIAS: Interviewer gender vs scores given =====
print("\n=== Technical Score by Interviewer Gender ===")
for ig in bias_int_data['interviewer_gender'].dropna().unique():
    subset = bias_int_data[bias_int_data['interviewer_gender'] == ig]['technical_score']
    print(f"{ig}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

ig_groups = [bias_int_data[bias_int_data['interviewer_gender'] == ig]['technical_score'].values 
             for ig in bias_int_data['interviewer_gender'].dropna().unique()]
if len(ig_groups) >= 2:
    f, p = f_oneway(*ig_groups)
    print(f"ANOVA by interviewer gender: F={f:.4f}, p={p:.6f}")

# ===== BIAS: Interaction of candidate and interviewer gender =====
print("\n=== Candidate × Interviewer Gender Mean Technical Score ===")
cross_gender = bias_int_data.dropna(subset=['candidate_gender', 'interviewer_gender'])
cross_gender = cross_gender[cross_gender['candidate_gender'].isin(['Male', 'Female'])]
cross_gender = cross_gender[cross_gender['interviewer_gender'].isin(['Male', 'Female'])]
cross_tab = cross_gender.groupby(['candidate_gender', 'interviewer_gender'])['technical_score'].agg(['mean', 'count', 'std'])
print(cross_tab)

# Male vs Female interviewers scoring Male vs Female candidates
for cand_g in ['Male', 'Female']:
    for int_g in ['Male', 'Female']:
        subset = cross_gender[(cross_gender['candidate_gender']==cand_g) & (cross_gender['interviewer_gender']==int_g)]['technical_score']
        print(f"Candidate {cand_g}, Interviewer {int_g}: mean={subset.mean():.3f}, n={len(subset)}")

# Statistical test: do male and female interviewers score differently?
male_int = bias_int_data[bias_int_data['interviewer_gender'] == 'Male']['technical_score']
female_int = bias_int_data[bias_int_data['interviewer_gender'] == 'Female']['technical_score']
t, p = ttest_ind(male_int, female_int, equal_var=False)
print(f"\nMale vs Female interviewer scores: t={t:.4f}, p={p:.6f}")

# ===== TIME OF DAY / DAY OF WEEK BIAS =====
print("\n=== Technical Score by Time of Day ===")
for tod in bias_int_data['interview_time_of_day'].dropna().unique():
    subset = bias_int_data[bias_int_data['interview_time_of_day'] == tod]['technical_score']
    print(f"{tod}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

print("\n=== Technical Score by Day of Week ===")
for dow in bias_int_data['interview_day_of_week'].dropna().unique():
    subset = bias_int_data[bias_int_data['interview_day_of_week'] == dow]['technical_score']
    print(f"{dow}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

# ===== INTERVIEWER LEVEL =====
print("\n=== Technical Score by Interviewer Level ===")
for level in bias_int_data['interviewer_level'].dropna().unique():
    subset = bias_int_data[bias_int_data['interviewer_level'] == level]['technical_score']
    print(f"{level}: mean={subset.mean():.3f}, std={subset.std():.3f}, n={len(subset)}")

# ===== VISUALIZATION =====
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Score by candidate gender
for i, g in enumerate(['Male', 'Female', 'Non-binary', 'Prefer not to say']):
    d = bias_int_data[bias_int_data['candidate_gender']==g]['technical_score']
    if len(d) > 0:
        axes[0,0].hist(d, alpha=0.5, label=g, bins=10)
axes[0,0].set_title('Technical Score by Candidate Gender')
axes[0,0].set_xlabel('Score')
axes[0,0].set_ylabel('Frequency')
axes[0,0].legend()

# 2. Score by candidate race
race_order = ['Asian', 'Black', 'Hispanic', 'Native American', 'Other', 'White']
for i, r in enumerate(race_order):
    d = bias_int_data[bias_int_data['candidate_race']==r]['technical_score']
    if len(d) > 0:
        axes[0,1].hist(d, alpha=0.5, label=r, bins=10)
axes[0,1].set_title('Technical Score by Candidate Race')
axes[0,1].set_xlabel('Score')
axes[0,1].set_ylabel('Frequency')
axes[0,1].legend()

# 3. Score by interviewer gender
int_genders = bias_int_data['interviewer_gender'].dropna().unique()
for ig in int_genders:
    d = bias_int_data[bias_int_data['interviewer_gender']==ig]['technical_score']
    axes[0,2].hist(d, alpha=0.5, label=ig, bins=10)
axes[0,2].set_title('Technical Score by Interviewer Gender')
axes[0,2].set_xlabel('Score')
axes[0,2].set_ylabel('Frequency')
axes[0,2].legend()

# 4. Score by interview time of day
tod_order = ['Morning', 'Midday', 'Afternoon', 'Evening']
for tod in tod_order:
    d = bias_int_data[bias_int_data['interview_time_of_day']==tod]['technical_score']
    if len(d) > 0:
        axes[1,0].hist(d, alpha=0.5, label=tod, bins=10)
axes[1,0].set_title('Technical Score by Time of Day')
axes[1,0].set_xlabel('Score')
axes[1,0].set_ylabel('Frequency')
axes[1,0].legend()

# 5. Score by interview day of week
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
for dow in dow_order:
    d = bias_int_data[bias_int_data['interview_day_of_week']==dow]['technical_score']
    if len(d) > 0:
        axes[1,1].hist(d, alpha=0.5, label=dow, bins=10)
axes[1,1].set_title('Technical Score by Day of Week')
axes[1,1].set_xlabel('Score')
axes[1,1].set_ylabel('Frequency')
axes[1,1].legend()

# 6. Hiring rate by candidate race
race_hiring_rate = bias_app_data.dropna(subset=['candidate_race']).groupby('candidate_race')['stage_hired'].mean()
axes[1,2].bar(race_hiring_rate.index, race_hiring_rate.values)
axes[1,2].set_title('Hire Rate by Candidate Race')
axes[1,2].set_xlabel('Race')
axes[1,2].set_ylabel('Hire Rate')
axes[1,2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/bias_analysis.png', dpi=120)
plt.close()

# ===== HIRING OUTCOME BY DEMOGRAPHICS =====
print("\n=== Hire Rate by Candidate Gender ===")
gender_hire = bias_app_data.dropna(subset=['candidate_gender']).groupby('candidate_gender')['stage_hired'].mean()
print(gender_hire)

print("\n=== Hire Rate by Candidate Race ===")
race_hire = bias_app_data.dropna(subset=['candidate_race']).groupby('candidate_race')['stage_hired'].mean()
print(race_hire)

print("\n=== Offer Rate by Candidate Race ===")
race_offer = bias_app_data.dropna(subset=['candidate_race']).groupby('candidate_race')['stage_offer'].mean()
print(race_offer)

# ===== COMPANY BACKGROUND × DEMOGRAPHICS INTERACTION =====
print("\n=== Company × Gender Distribution ===")
cat_gender = db.frame(db.query("""
SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat,
  a.candidate_gender
FROM greenhouse__application_enhanced a
"""))
ct = pd.crosstab(cat_gender['company_cat'], cat_gender['candidate_gender'])
print(ct)

# Also check if the FAANG effect is confounded with demographics
# Load data with both company category and demographics
bias_model_data = db.frame(db.query("""
SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat,
  a.candidate_gender, a.candidate_race, a.education_level, a.years_of_experience,
  a.skill_count, a.university_tier, a.stage_hired
FROM greenhouse__application_enhanced a
"""))
print(f"\nBias model data: {bias_model_data.shape}")
print(bias_model_data['candidate_gender'].value_counts(dropna=False))

print("\nBias analysis complete.")
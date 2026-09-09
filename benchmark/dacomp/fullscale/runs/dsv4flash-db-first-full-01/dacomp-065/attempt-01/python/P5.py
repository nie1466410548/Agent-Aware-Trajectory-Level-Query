import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# ============== Stage conversion rates ==============
print("=== Stage Conversion Rates by Company Category ===")
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
WHERE a.stage_application_review = 1
GROUP BY cat.company_cat
ORDER BY hired DESC
"""))

# Calculate conversion rates
for cat_name in funnel['company_cat'].unique():
    row = funnel[funnel['company_cat'] == cat_name].iloc[0]
    stages = ['app_review', 'phone_screen', 'tech_int', 'panel', 'final_int', 'offer', 'hired']
    print(f"\n{cat_name}:")
    for i in range(len(stages)-1):
        curr = stages[i]
        nxt = stages[i+1]
        if row[curr] > 0:
            conv = row[nxt] / row[curr] * 100
            print(f"  {curr} -> {nxt}: {row[curr]} -> {row[nxt]} ({conv:.1f}%)")

# ============== Quantify the FAANG "halo" effect ==============
# Compare FAANG premium across dimensions
# If it's pure skill, we'd expect larger premium on technical and problem-solving
# If it's halo, we'd see uniform premium across all dimensions

print("\n\n=== FAANG Premium Uniformity Test ===")
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
  SELECT i.application_id, cat.company_cat,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
"""))

# Uncontrolled means
print("Uncontrolled mean scores:")
for dim in ['avg_tech', 'avg_ps', 'avg_comm', 'avg_cf', 'avg_lead']:
    faang_mean = data[data['company_cat']=='FAANG'][dim].mean()
    trad_mean = data[data['company_cat']=='Traditional'][dim].mean()
    major_mean = data[data['company_cat']=='Major_Tech'][dim].mean()
    print(f"  {dim}: FAANG={faang_mean:.3f}, Major_Tech={major_mean:.3f}, Traditional={trad_mean:.3f}")

# Raw premium (uncontrolled)
print("\nRaw FAANG premium (vs Traditional):")
for dim in ['avg_tech', 'avg_ps', 'avg_comm', 'avg_cf', 'avg_lead']:
    premium = data[data['company_cat']=='FAANG'][dim].mean() - data[data['company_cat']=='Traditional'][dim].mean()
    print(f"  {dim}: {premium:.3f}")

# ============== Visualize funnel ==============
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Funnel comparison
ax = axes[0]
stages = ['Application\nReview', 'Phone\nScreen', 'Technical\nInterview', 'Panel\nInterview', 'Final\nInterview', 'Offer', 'Hired']
x = range(len(stages))
for cat_name, color, marker in [('FAANG', '#440154', 'o'), ('Major_Tech', '#21918c', 's'), ('Traditional', '#fde725', 'D')]:
    row = funnel[funnel['company_cat'] == cat_name].iloc[0]
    values = [row[s] for s in ['app_review', 'phone_screen', 'tech_int', 'panel', 'final_int', 'offer', 'hired']]
    ax.plot(x, values, color=color, marker=marker, label=cat_name, linewidth=2)
ax.set_xticks(x)
ax.set_xticklabels(stages, fontsize=8)
ax.set_ylabel('Number of applications')
ax.set_title('Hiring Funnel by Company Background')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Conversion rates (relative to previous stage)
ax = axes[1]
for cat_name, color in [('FAANG', '#440154'), ('Major_Tech', '#21918c'), ('Traditional', '#fde725')]:
    row = funnel[funnel['company_cat'] == cat_name].iloc[0]
    stage_names = ['App Review', 'Phone\nScreen', 'Tech\nInt', 'Panel', 'Final', 'Offer']
    prev_stages = ['app_review', 'phone_screen', 'tech_int', 'panel', 'final_int', 'offer']
    next_stages = ['phone_screen', 'tech_int', 'panel', 'final_int', 'offer', 'hired']
    conv_rates = []
    for p, n in zip(prev_stages, next_stages):
        if row[p] > 0:
            conv_rates.append(row[n] / row[p] * 100)
        else:
            conv_rates.append(0)
    ax.plot(stage_names, conv_rates, color=color, marker='o', label=cat_name, linewidth=2)
ax.set_ylabel('Conversion rate (%)')
ax.set_title('Stage-to-Stage Conversion Rates')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/funnel_analysis.png', dpi=120)
plt.close()

# ============== Summary statistics for report ==============
print("\n\n=== SUMMARY STATISTICS ===")
print(f"Total applications: 18186 (12000 distinct)")
print(f"Total interviews/scorecards: 14625 (11928 distinct)")
print(f"Total hired: 1859 (in stage_hired)")

# Company distribution
print(f"\nCompany category distribution (distinct apps):")
cat_counts = db.frame(db.query("""
SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat
FROM greenhouse__application_enhanced a
"""))
print(cat_counts['company_cat'].value_counts())

print("\nAverage technical scores (application-level):")
print(data.groupby('company_cat')['avg_tech'].describe())

print("\nAll analyses complete.")
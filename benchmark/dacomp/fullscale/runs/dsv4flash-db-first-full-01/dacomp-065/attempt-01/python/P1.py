import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, kruskal, pearsonr

# Load application-level data
app_data = db.frame(db.query("""
WITH cat AS (
  SELECT application_id,
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

print(f"App-level data shape: {app_data.shape}")
print(app_data['company_cat'].value_counts())
print(app_data.groupby('company_cat')['avg_tech'].describe())

# ANOVA for technical scores by company category
faang_tech = app_data[app_data['company_cat'] == 'FAANG']['avg_tech'].dropna()
major_tech = app_data[app_data['company_cat'] == 'Major_Tech']['avg_tech'].dropna()
trad_tech = app_data[app_data['company_cat'] == 'Traditional']['avg_tech'].dropna()

f_stat, p_value = f_oneway(faang_tech, major_tech, trad_tech)
print(f"\n=== ANOVA: Technical Score by Company Category ===")
print(f"F-statistic: {f_stat:.4f}, p-value: {p_value:.6f}")

# Kruskal-Wallis (non-parametric)
h_stat, kw_p = kruskal(faang_tech, major_tech, trad_tech)
print(f"Kruskal-Wallis H: {h_stat:.4f}, p-value: {kw_p:.6f}")

# Pairwise t-tests
from scipy.stats import ttest_ind
print("\n=== Pairwise t-tests ===")
for name1, g1 in [('FAANG', faang_tech), ('Major_Tech', major_tech), ('Traditional', trad_tech)]:
    for name2, g2 in [('FAANG', faang_tech), ('Major_Tech', major_tech), ('Traditional', trad_tech)]:
        if name1 < name2:
            t, p = ttest_ind(g1, g2, equal_var=False)
            print(f"{name1} vs {name2}: t={t:.4f}, p={p:.6f}")

# Effect sizes (Cohen's d)
def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    s1, s2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    sp = np.sqrt(((n1-1)*s1 + (n2-1)*s2) / (n1+n2-2))
    return (np.mean(g1) - np.mean(g2)) / sp

print("\n=== Cohen's d effect sizes ===")
for name1, g1 in [('FAANG', faang_tech), ('Major_Tech', major_tech), ('Traditional', trad_tech)]:
    for name2, g2 in [('FAANG', faang_tech), ('Major_Tech', major_tech), ('Traditional', trad_tech)]:
        if name1 < name2:
            d = cohens_d(g1, g2)
            print(f"{name1} vs {name2}: d={d:.4f}")

# Boxplot
plt.figure(figsize=(10, 6))
order = ['FAANG', 'Major_Tech', 'Traditional']
sns.boxplot(x='company_cat', y='avg_tech', data=app_data, order=order, palette='viridis')
plt.title('Technical Interview Score by Company Background', fontsize=14)
plt.xlabel('Company Category', fontsize=12)
plt.ylabel('Average Technical Score (1-10)', fontsize=12)
plt.tight_layout()
plt.savefig('/work/tech_score_by_company.png', dpi=120)
plt.close()

# Also check problem solving scores
f_ps, p_ps = f_oneway(
    app_data[app_data['company_cat']=='FAANG']['avg_ps'].dropna(),
    app_data[app_data['company_cat']=='Major_Tech']['avg_ps'].dropna(),
    app_data[app_data['company_cat']=='Traditional']['avg_ps'].dropna()
)
print(f"\n=== ANOVA: Problem Solving Score by Company Category ===")
print(f"F-statistic: {f_ps:.4f}, p-value: {p_ps:.6f}")

# Positive recommendation rate by category
print("\n=== Positive Recommendation Rate ===")
print(app_data.groupby('company_cat')['ever_pos_rec'].mean())

# Chi-square for recommendation rate
from scipy.stats import chi2_contingency
contingency = pd.crosstab(app_data['company_cat'], app_data['ever_pos_rec'])
chi2, p_chi, dof, expected = chi2_contingency(contingency)
print(f"Chi-square: {chi2:.4f}, p-value: {p_chi:.6f}")

print("\nAnalysis complete.")
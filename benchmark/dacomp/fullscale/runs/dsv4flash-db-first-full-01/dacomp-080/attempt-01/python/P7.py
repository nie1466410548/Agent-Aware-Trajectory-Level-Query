import pandas as pd, numpy as np

prof = pd.read_csv('/work/user_scored.csv')

# ---- Value distribution by language ----
lang_agg = prof.groupby('dom_lang').agg(
    n_users=('email','count'),
    avg_score=('value_score','mean'),
    med_score=('value_score','median'),
    avg_freq=('n_survey_responses','mean'),
    avg_completion=('completion_rate','mean'),
    avg_channels=('n_channels','mean'),
    pct_high_power=('tier', lambda s: 100*(s.isin(['high_value','power_user'])).mean()),
    pct_power=('tier', lambda s: 100*(s=='power_user').mean()),
    pct_one_time=('tier', lambda s: 100*(s=='one_time').mean())
).sort_values('avg_score', ascending=False)
print("=== Value by language ===")
print(lang_agg.round(1).to_string())

# ---- Value distribution by region/continent ----
region_agg = prof.groupby('continent').agg(
    n_users=('email','count'),
    avg_score=('value_score','mean'),
    med_score=('value_score','median'),
    avg_freq=('n_survey_responses','mean'),
    avg_completion=('completion_rate','mean'),
    avg_channels=('n_channels','mean'),
    pct_high_power=('tier', lambda s: 100*(s.isin(['high_value','power_user'])).mean()),
    pct_power=('tier', lambda s: 100*(s=='power_user').mean()),
    pct_one_time=('tier', lambda s: 100*(s=='one_time').mean())
).sort_values('avg_score', ascending=False)
print("\n=== Value by region ===")
print(region_agg.round(1).to_string())

# ---- Cross-tab: tier x language (as % of each language) ----
ct_lang = pd.crosstab(prof.dom_lang, prof.tier, normalize='index')*100
print("\n=== Tier composition by language (row %) ===")
print(ct_lang.round(1).to_string())

# ---- Cross-tab: tier x region (as % of each region) ----
ct_reg = pd.crosstab(prof.continent, prof.tier, normalize='index')*100
print("\n=== Tier composition by region (row %) ===")
print(ct_reg.round(1).to_string())

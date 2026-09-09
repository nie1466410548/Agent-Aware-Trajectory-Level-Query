import pandas as pd, numpy as np
from scipy.stats import chi2_contingency, ttest_ind

prof = pd.read_csv('/work/user_scored.csv')

# ---- Chi-square: tier vs language and tier vs region ----
ct1 = pd.crosstab(prof.dom_lang, prof.tier)
chi2, p, dof, _ = chi2_contingency(ct1)
print(f"Tier × Language chi2 = {chi2:.1f}, p = {p:.5f}")

ct2 = pd.crosstab(prof.continent, prof.tier)
chi2b, pb, dof2, _ = chi2_contingency(ct2)
print(f"Tier × Continent chi2 = {chi2b:.1f}, p = {pb:.5f}")

# ---- Transition "path" profile: gap between medium and high users ----
print("\n=== Medium→High gap (High - Medium) by Language ===")
lang_gap = []
for lang in sorted(prof.dom_lang.unique()):
    sub = prof[prof.dom_lang == lang]
    m = sub[sub.tier == 'medium_value']
    h = sub[sub.tier == 'high_value']
    if len(m) > 20 and len(h) > 20:
        lang_gap.append({
            'language': lang,
            'n_medium': len(m),
            'n_high': len(h),
            'gap_freq': round(h.n_survey_responses.mean() - m.n_survey_responses.mean(), 3),
            'gap_completion': round(h.completion_rate.mean() - m.completion_rate.mean(), 3),
            'gap_channels': round(h.n_channels.mean() - m.n_channels.mean(), 3),
            'gap_score': round(h.value_score.mean() - m.value_score.mean(), 3),
            'p_val_freq': round(ttest_ind(h.n_survey_responses, m.n_survey_responses, equal_var=False).pvalue, 6),
            'p_val_completion': round(ttest_ind(h.completion_rate, m.completion_rate, equal_var=False).pvalue, 6),
            'p_val_channels': round(ttest_ind(h.n_channels, m.n_channels, equal_var=False).pvalue, 6)
        })
gap_df = pd.DataFrame(lang_gap).set_index('language')
print(gap_df.to_string())

print("\n=== Medium→High gap by Continent ===")
cont_gap = []
for cont in sorted(prof.continent.unique()):
    sub = prof[prof.continent == cont]
    m = sub[sub.tier == 'medium_value']
    h = sub[sub.tier == 'high_value']
    if len(m) > 20 and len(h) > 20:
        cont_gap.append({
            'continent': cont,
            'n_medium': len(m),
            'n_high': len(h),
            'gap_freq': round(h.n_survey_responses.mean() - m.n_survey_responses.mean(), 3),
            'gap_completion': round(h.completion_rate.mean() - m.completion_rate.mean(), 3),
            'gap_channels': round(h.n_channels.mean() - m.n_channels.mean(), 3),
            'gap_score': round(h.value_score.mean() - m.value_score.mean(), 3),
            'p_val_freq': round(ttest_ind(h.n_survey_responses, m.n_survey_responses, equal_var=False).pvalue, 6),
            'p_val_completion': round(ttest_ind(h.completion_rate, m.completion_rate, equal_var=False).pvalue, 6),
            'p_val_channels': round(ttest_ind(h.n_channels, m.n_channels, equal_var=False).pvalue, 6)
        })
cont_gap_df = pd.DataFrame(cont_gap).set_index('continent')
print(cont_gap_df.to_string())

# ---- Segmentation summary for the report ----
print("\n\n=== Segmentation Summary ===")
seg = prof.groupby('tier').agg(
    n_users=('email','count'),
    pct_users=('email', lambda s: f"{100*len(s)/len(prof):.1f}%"),
    avg_score=('value_score','mean'),
    avg_freq=('n_survey_responses','mean'),
    avg_completion=('completion_rate','mean'),
    avg_channels=('n_channels','mean'),
    pct_total_responses=('n_survey_responses', lambda s: f"{100*s.sum()/prof.n_survey_responses.sum():.1f}%"),
    pct_total_completed=('n_completed', lambda s: f"{100*s.sum()/prof.n_completed.sum():.1f}%")
).loc[['one_time','low_value','medium_value','high_value','power_user']]
print(seg.to_string())
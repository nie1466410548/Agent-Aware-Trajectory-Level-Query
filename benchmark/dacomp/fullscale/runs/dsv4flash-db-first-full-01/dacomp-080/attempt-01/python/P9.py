import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from scipy.stats import chi2_contingency

prof = pd.read_csv('/work/user_scored.csv')

# ---- Logistic regression: medium(0) vs high(1) ----
mh = prof[prof.tier.isin(['medium_value', 'high_value'])].copy()
mh['label'] = (mh.tier == 'high_value').astype(int)

features = ['n_survey_responses', 'completion_rate', 'n_channels', 
            'avg_progress', 'active_months']
X = mh[features].copy()
y = mh['label'].values

scaler = StandardScaler()
Xs = scaler.fit_transform(X)
lr = LogisticRegression(max_iter=1000, C=1.0)
lr.fit(Xs, y)
auc = roc_auc_score(y, lr.predict_proba(Xs)[:, 1])

print("=== Logistic Regression: P(high_value) | medium or high ===")
print("AUC:", round(auc, 3))
for f, coef in zip(features, lr.coef_[0]):
    print(f"  {f:25s} std-coef = {coef:+.3f}  odds-ratio per 1 SD = {np.exp(coef):.2f}")

# ---- Chi-square: tier vs language and tier vs region ----
ct1 = pd.crosstab(prof.dom_lang, prof.tier)
chi2, p, dof, _ = chi2_contingency(ct1)
print(f"\nTier × Language chi2 = {chi2:.1f}, p = {p:.5f}")

ct2 = pd.crosstab(prof.continent, prof.tier)
chi2b, pb, dof2, _ = chi2_contingency(ct2)
print(f"Tier × Continent chi2 = {chi2b:.1f}, p = {pb:.5f}")

# ---- Transition "path" profile: how far each language/region is from its medium baseline ----
# For each language, compare medium vs high on the three core drivers
print("\n=== Medium→High gap (High - Medium) by Language ===")
lang_gap = []
for lang in sorted(prof.dom_lang.unique()):
    sub = prof[prof.dom_lang == lang]
    m = sub[sub.tier == 'medium_value']
    h = sub[sub.tier == 'high_value']
    if len(m) > 20 and len(h) > 20:
        lang_gap.append({
            'language': lang,
            'gap_freq': h.n_survey_responses.mean() - m.n_survey_responses.mean(),
            'gap_completion': h.completion_rate.mean() - m.completion_rate.mean(),
            'gap_channels': h.n_channels.mean() - m.n_channels.mean(),
            'gap_score': h.value_score.mean() - m.value_score.mean()
        })
print(pd.DataFrame(lang_gap).set_index('language').round(3).to_string())

print("\n=== Medium→High gap by Continent ===")
cont_gap = []
for cont in sorted(prof.continent.unique()):
    sub = prof[prof.continent == cont]
    m = sub[sub.tier == 'medium_value']
    h = sub[sub.tier == 'high_value']
    if len(m) > 20 and len(h) > 20:
        cont_gap.append({
            'continent': cont,
            'gap_freq': h.n_survey_responses.mean() - m.n_survey_responses.mean(),
            'gap_completion': h.completion_rate.mean() - m.completion_rate.mean(),
            'gap_channels': h.n_channels.mean() - m.n_channels.mean(),
            'gap_score': h.value_score.mean() - m.value_score.mean()
        })
print(pd.DataFrame(cont_gap).set_index('continent').round(3).to_string())

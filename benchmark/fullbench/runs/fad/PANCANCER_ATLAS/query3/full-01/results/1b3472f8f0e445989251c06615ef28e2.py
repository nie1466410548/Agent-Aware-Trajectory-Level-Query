import json
import pandas as pd

clin = pd.DataFrame(json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query3/full-01/results/27979943806b4743ba1654259e35f8c5.json')))
mut = pd.DataFrame(json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query3/full-01/results/a9efce12f6c14f04bff12ac6e0635c09.json')))

print("clinical rows:", len(clin), "unique patient_id:", clin['patient_id'].nunique())
# dedupe just in case (same patient, same histology)
clin = clin.drop_duplicates(subset=['patient_id'])

# mutation carriers: map ParticipantBarcode suffix (TCGA-XX-YYYY -> YYYY)
mut['pid'] = mut['ParticipantBarcode'].str.split('-').str[-1]
print("mutation carriers:", len(mut), "unique suffixes:", mut['pid'].nunique())

cdh1 = set(mut['pid'])
clin['cdh1_mut'] = clin['patient_id'].isin(cdh1)

ct = pd.crosstab(clin['histological_type'], clin['cdh1_mut'])
ct.columns = ['No_CDH1_Mut', 'CDH1_Mut']
ct['Total'] = ct.sum(axis=1)
print("\nFull contingency table:")
print(ct)

# exclude categories with marginal totals <= 10
ct2 = ct[ct['Total'] > 10][['No_CDH1_Mut', 'CDH1_Mut']]
print("\nFiltered contingency table (row totals > 10):")
print(ct2)

obs = ct2.values.astype(float)
row_tot = obs.sum(axis=1, keepdims=True)
col_tot = obs.sum(axis=0, keepdims=True)
grand = obs.sum()
exp = row_tot @ col_tot / grand
chi2 = ((obs - exp) ** 2 / exp).sum()
dof = (obs.shape[0] - 1) * (obs.shape[1] - 1)
print("\nN =", int(grand), " dof =", dof)
print("Chi-square statistic =", chi2)
print("rounded:", round(chi2, 4))

# p-value via survival function of chi2 (using series expansion from stdlib is hard; use scipy if available)
try:
    from scipy.stats import chi2 as chi2dist
    print("p-value =", chi2dist.sf(chi2, dof))
except Exception as e:
    print("scipy unavailable:", e)

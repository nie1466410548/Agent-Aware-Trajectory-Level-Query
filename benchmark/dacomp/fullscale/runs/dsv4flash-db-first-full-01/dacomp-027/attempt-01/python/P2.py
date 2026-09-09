import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/full_joined.csv')

# 1. Pearson correlations between Secincident Count and numeric variables
num_cols = ['affected','displaced','injured','casualties','missing','damage_pct','power_pct','water_pct',
            'recycling','carbon','renewable','wqi','sanitation','vaccination',
            'duration','fund_util','resource_gap','delivery','deliv_time','stk_sat','pub_perm','report_comp']

corrs = []
for col in num_cols:
    r, p = stats.pearsonr(df['Secincident Count'].values, df[col].values)
    corrs.append({'var': col, 'pearson_r': round(r,4), 'p_value': round(p,6), 'sig': p < 0.05})
corr_df = pd.DataFrame(corrs).sort_values('pearson_r', key=abs, ascending=False)
print(corr_df.to_string(index=False))

# 2. Spearman correlations (non-linear monotonic)
spears = []
for col in num_cols:
    r, p = stats.spearmanr(df['Secincident Count'].values, df[col].values)
    spears.append({'var': col, 'spearman_r': round(r,4), 'p_value': round(p,6), 'sig': p < 0.05})
sp_df = pd.DataFrame(spears).sort_values('spearman_r', key=abs, ascending=False)
print("\n=== Spearman ===")
print(sp_df.to_string(index=False))

# 3. ANOVA: Secincident Count groups vs Environmental Impact Rate
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low(0-32)','Med(33-65)','High(66-100)'])
groups = [g['wqi'].values for _, g in df.groupby('sec_group')]
f, p = stats.f_oneway(*groups)
print(f"\nANOVA: WQI ~ sec_group -> F={f:.3f}, p={p:.6f}")

groups2 = [g['sanitation'].values for _, g in df.groupby('sec_group')]
f2, p2 = stats.f_oneway(*groups2)
print(f"ANOVA: Sanitation ~ sec_group -> F={f2:.3f}, p={p2:.6f}")

# 4. Chi-square: Environmental Impact Rate vs sec_group
ct = pd.crosstab(df['sec_group'], df['Environmental Impact Rate'])
chi2, p_chi, dof, expected = stats.chi2_contingency(ct)
print(f"\nChi-square: Environmental Impact Rate vs sec_group -> chi2={chi2:.3f}, p={p_chi:.4f}")
print(ct)

# 5. Chi-square: Disease Risk vs sec_group
ct2 = pd.crosstab(df['sec_group'], df['Disease Risk'])
chi2_2, p_chi2, _, _ = stats.chi2_contingency(ct2)
print(f"\nChi-square: Disease Risk vs sec_group -> chi2={chi2_2:.3f}, p={p_chi2:.4f}")
print(ct2)

# 6. Chi-square: Mental Health Assistance vs sec_group
ct3 = pd.crosstab(df['sec_group'], df['mental'])
chi2_3, p_chi3, _, _ = stats.chi2_contingency(ct3)
print(f"\nChi-square: Mental Health vs sec_group -> chi2={chi2_3:.3f}, p={p_chi3:.4f}")
print(ct3)

# 7. Disaster Level vs Environmental Impact Rate
ct4 = pd.crosstab(df['Disaster Level'], df['Environmental Impact Rate'])
chi2_4, p_chi4, _, _ = stats.chi2_contingency(ct4)
print(f"\nChi-square: Disaster Level vs Environmental Impact Rate -> chi2={chi2_4:.3f}, p={p_chi4:.4f}")
print(ct4)

# 8. Disaster Level vs Disease Risk
ct5 = pd.crosstab(df['Disaster Level'], df['Disease Risk'])
chi2_5, p_chi5, _, _ = stats.chi2_contingency(ct5)
print(f"\nChi-square: Disaster Level vs Disease Risk -> chi2={chi2_5:.3f}, p={p_chi5:.4f}")
print(ct5)
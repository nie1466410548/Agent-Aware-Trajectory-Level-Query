import pandas as pd
import numpy as np
from scipy import stats

sql = """
SELECT s."Medical history" AS medhx, s."Health status" AS hs,
  s."Smoking status" AS smoke, s."Drinking Status" AS drink
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
df = db.frame(db.query(sql))

# Chi-square tests
for col, name in [('hs','Health status'), ('smoke','Smoking status'), ('drink','Drinking status')]:
    ct = pd.crosstab(df['medhx'], df[col])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    # Cramer's V
    n = ct.values.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    print(f"{name}: chi2={chi2:.1f}, p={p:.3e}, Cramer's V={cramers_v:.3f}")
    print(ct.div(ct.sum(axis=1), axis=0).round(3).to_string())
    print()
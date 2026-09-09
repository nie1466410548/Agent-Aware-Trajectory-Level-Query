import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

baseline_comp = pd.read_csv('/work/baseline_compliance.csv', header=None, index_col=0)
baseline_comp = baseline_comp.iloc[:, 0]
final_comp = pd.read_csv('/work/final_compliance_series.csv', index_col=0)
final_comp = final_comp.iloc[:, 0]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(baseline_comp, bins=20, alpha=0.7, color='coral', edgecolor='black')
axes[0].axvline(0.6, color='green', linestyle='--', linewidth=2, label='60% threshold')
axes[0].set_xlabel('% in Top 3 Industries')
axes[0].set_ylabel('Number of Reps')
axes[0].set_title(f'Baseline Industry Compliance\n{(baseline_comp >= 0.6).sum()}/1000 reps meet 60% rule')
axes[0].legend()

axes[1].hist(final_comp, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
axes[1].axvline(0.6, color='green', linestyle='--', linewidth=2, label='60% threshold')
axes[1].set_xlabel('% in Top 3 Industries')
axes[1].set_ylabel('Number of Reps')
axes[1].set_title(f'Final Industry Compliance\n{(final_comp >= 0.6).sum()}/1000 reps meet 60% rule')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/industry_compliance.png', dpi=150)
plt.close()
print("saved industry_compliance.png")
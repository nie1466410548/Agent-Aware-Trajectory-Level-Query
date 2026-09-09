import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Resource Allocation Status
labels_ras = ['Sufficient (74)', 'Critical (65)', 'Limited (63)']
vals_ras = [74, 65, 63]
colors_ras = ['#2ecc71', '#e74c3c', '#f39c12']
axes[0].pie(vals_ras, labels=labels_ras, colors=colors_ras, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Resource Allocation Status (Level 5)')

# Supply Flow Status
labels_sfs = ['Stable (78)', 'Disrupted (69)', 'Strained (55)']
vals_sfs = [78, 69, 55]
colors_sfs = ['#2ecc71', '#e74c3c', '#f39c12']
axes[1].pie(vals_sfs, labels=labels_sfs, colors=colors_sfs, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Supply Flow Status (Level 5)')

# Last-Mile Delivery Status
labels_lm = ['Delayed (73)', 'Suspended (65)', 'On Track (64)']
vals_lm = [73, 65, 64]
colors_lm = ['#e74c3c', '#f39c12', '#2ecc71']
axes[2].pie(vals_lm, labels=labels_lm, colors=colors_lm, autopct='%1.1f%%', startangle=90)
axes[2].set_title('Last-Mile Delivery Status (Level 5)')

plt.tight_layout()
plt.savefig('/work/fig2_operational_status.png', dpi=150)
plt.close()
print('fig2 regenerated')
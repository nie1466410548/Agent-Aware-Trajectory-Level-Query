import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 12, 'figure.dpi': 120, 'figure.facecolor': 'white'})

# ============== 6. Email Intensity Analysis ==============
intensity = ['<20\nemails/mo', '20-30\nemails/mo', '30-40\nemails/mo', '40+\nemails/mo']
n_i = [428, 638, 113, 13]
orders_i = [0.62, 1.78, 3.37, 5.00]
open_i = [39.1, 42.0, 58.5, 61.0]
prr_i = [0.99, 0.94, 0.93, 0.82]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
x = np.arange(len(intensity))

ax = axes[0]
bars = ax.bar(x, orders_i, color=['#95a5a6','#3498db','#2ecc71','#e67e22'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(intensity)
ax.set_title('Orders by Email Intensity', fontweight='bold')
ax.set_ylabel('Avg Orders'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(orders_i): ax.text(i, v+0.1, f'{v:.2f}', ha='center', fontweight='bold')

ax = axes[1]
bars = ax.bar(x, open_i, color=['#95a5a6','#3498db','#2ecc71','#e67e22'], width=0.6)
ax.set_xticks(x); ax.set_xticklabels(intensity)
ax.set_title('Email Open Rate by Intensity', fontweight='bold')
ax.set_ylabel('Open Rate (%)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(open_i): ax.text(i, v+0.8, f'{v:.1f}%', ha='center', fontweight='bold')

ax = axes[2]
ax.plot(x, prr_i, 'o-', color='#e74c3c', linewidth=2.5, markersize=10)
ax.set_xticks(x); ax.set_xticklabels(intensity)
ax.set_title('Paid Retention Rate by Intensity', fontweight='bold')
ax.set_ylabel('Retention Rate'); ax.grid(True, alpha=0.3); ax.set_ylim(0.75, 1.02)
for i,v in enumerate(prr_i): ax.text(i, v+0.01, f'{v:.3f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/email_intensity.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved")

# ============== 7. Touchpoint Path / Cadence ==============
# Typical weekly sequence of touches (18-day cycle per type)
types = ['PROMO', 'NEWS', 'FLASH', 'WINBK', 'LAUNCH', 'SURVEY', 'VIP', 'DIGEST']
metrics = {'PROMO': (0.91, 40.9), 'NEWS': (0.48, 36.0), 'FLASH': (0.67, 27.0),
           'WINBK': (0.20, 22.0), 'LAUNCH': (1.74, 48.0), 'SURVEY': (0.45, 32.0),
           'VIP': (3.68, 52.0), 'DIGEST': (0.80, 34.0)}
gmv = [metrics[t][0] for t in types]
opn = [metrics[t][1] for t in types]
colors = ['#2ecc71' if t != 'WINBK' else '#e74c3c' for t in types]

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Path visualization: bubble chart along cycle
ax = axes[0]
bubble_sizes = [m*900 for m in gmv]
sc = ax.scatter(np.arange(len(types)), np.ones(len(types)), s=bubble_sizes, c=opn, cmap='RdYlGn', alpha=0.8, vmin=15, vmax=55)
ax.set_xticks(np.arange(len(types))); ax.set_xticklabels(types)
ax.set_yticks([])
ax.set_title('Typical 18-Day Touchpoint Cycle\n(bubble size = GMV/received, color = open rate %)', fontweight='bold')
ax.annotate('Weekly WINBACK is the\nworst performer', xy=(3, 1), xytext=(0.5, -1.8),
            arrowprops=dict(arrowstyle='->', color='#e74c3c'), color='#e74c3c', fontweight='bold', fontsize=10)
ax.set_xlim(-0.5, 7.5); ax.set_ylim(-2, 2.5)
cbar = plt.colorbar(sc, ax=ax, orientation='horizontal', pad=0.3); cbar.set_label('Open rate (%)')

# Efficiency bar for the cycle
ax = axes[1]
bars = ax.bar(np.arange(len(types)), gmv, color=['#2ecc71' if t!='WINBK' else '#e74c3c' for t in types], width=0.6)
ax.set_xticks(np.arange(len(types))); ax.set_xticklabels(types)
ax.set_title('GMV per Email Received in Cycle', fontweight='bold')
ax.set_ylabel('GMV per received ($)'); ax.grid(axis='y', alpha=0.3)
for i,v in enumerate(gmv): ax.text(i, v+0.05, f'${v:.2f}', ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('/work/touchpoint_path.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 7 saved")
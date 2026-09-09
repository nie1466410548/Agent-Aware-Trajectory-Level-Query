import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load(sid, cols):
    rows=[]
    with open(f'/results/S{sid}.rows.jsonl') as f:
        for line in f: rows.append(json.loads(line))
    return pd.DataFrame(rows, columns=cols)

def todict(df, keycol, valcol):
    return {row[keycol]: float(row[valcol]) for _, row in df.iterrows()}

sleep_d = todict(load(14, ['Sleep duration','total','yes_n','yes_pct']), 'Sleep duration', 'yes_pct')
diet_d  = todict(load(15, ['diet_group','total','yes_n','yes_pct']), 'diet_group', 'yes_pct')
acad_d  = todict(load(16, ['acad_group','total','yes_n','yes_pct']), 'acad_group', 'yes_pct')
fin_d   = todict(load(17, ['fin_group','total','yes_n','yes_pct']), 'fin_group', 'yes_pct')
risk_df = load(29, ['n_risk','total','yes_n','yes_pct'])
ds_df   = load(25, ['Dietary habits','sleep_cat','total','yes_n','yes_pct'])
print("diet keys:", list(diet_d.keys()))

order_acad  = ['Low (1-2)','Medium (3)','High (4-5)']
order_fin   = ['Low (1-2)','Medium (3)','High (4-5)']
order_diet  = ['Healthy','Moderate','Unhealthy']
order_sleep = ['More than 8 hours','7-8 hours','5-6 hours','Less than 5 hours']

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

def bar(ax, labels, vals, title, color):
    ax.bar(range(len(labels)), vals, color=color, edgecolor='black')
    for i,v in enumerate(vals): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=20, ha='right', fontsize=10)
    ax.set_ylabel('With suicidal thoughts (%)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(62.8, color='gray', ls='--', lw=1)
    ax.text(len(labels)-0.02, 64.5, 'overall 62.8%', color='gray', fontsize=9, ha='right')
    ax.grid(axis='y', alpha=0.3)

bar(axes[0,0], order_acad,  [acad_d[l] for l in order_acad],  'Academic stress', '#C44E52')
bar(axes[0,1], order_fin,   [fin_d[l] for l in order_fin],     'Financial (economic) stress', '#DD8452')
bar(axes[0,2], order_diet,  [diet_d[l] for l in order_diet],   'Dietary habits', '#55A868')
bar(axes[1,0], order_sleep, [sleep_d[l] for l in order_sleep], 'Sleep duration', '#8172B3')

# Diet x sleep heatmap
mat = np.array([[float(ds_df.loc[(ds_df['Dietary habits']==d)&(ds_df['sleep_cat']==s),'yes_pct'].iloc[0])
                 for s in ['Sleep<5h','Sleep>=5h']] for d in ['Healthy','Moderate','Unhealthy']])
im = axes[1,1].imshow(mat, cmap='YlOrRd', vmin=50, vmax=80, aspect='auto')
axes[1,1].set_xticks([0,1]); axes[1,1].set_xticklabels(['<5 h sleep','≥5 h sleep'], fontsize=10)
axes[1,1].set_yticks([0,1,2]); axes[1,1].set_yticklabels(['Healthy','Moderate','Unhealthy'], fontsize=10)
for i in range(3):
    for j in range(2):
        axes[1,1].text(j, i, f"{mat[i,j]:.1f}%", ha='center', va='center', fontsize=11, fontweight='bold')
axes[1,1].set_title('Diet × Sleep: prevalence (%)', fontsize=12, fontweight='bold')
axes[1,1].set_xlabel('Sleep'); axes[1,1].set_ylabel('Diet')

# Risk-factor dose response
ax = axes[1,2]
vals = [float(risk_df.loc[risk_df['n_risk']==k,'yes_pct'].iloc[0]) for k in [0,1,2,3,4]]
ax.bar(range(5), vals, color='#C44E52', edgecolor='black')
for i,v in enumerate(vals): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_xticks(range(5)); ax.set_xticklabels(['0','1','2','3','4'])
ax.set_ylim(0,100); ax.grid(axis='y', alpha=0.3)
ax.set_ylabel('With suicidal thoughts (%)'); ax.set_xlabel('Number of risk factors')
ax.set_title('Dose–response: risk-factor count\n(academic≥4, financial≥4, unhealthy diet, sleep<5h)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/student_suicidal_ideation_characteristics.png', dpi=130, bbox_inches='tight')
print("Saved figure 1")

scen_labels = ['Protective\n(low stress,\nhealthy)','High financial\nstress only','High academic\nstress only','High both\nstresses','High both +\nunhealthy diet\n+ <5h sleep']
scen_probs = [0.256, 0.584, 0.488, 0.848, 0.909]
fig2, ax2 = plt.subplots(figsize=(9,5))
ax2.bar(range(len(scen_labels)), scen_probs, color=['#55A868','#DD8452','#4C72B0','#C44E52','#8B0000'], edgecolor='black')
for i,v in enumerate(scen_probs): ax2.text(i, v+0.01, f'{v*100:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax2.set_xticks(range(len(scen_labels))); ax2.set_xticklabels(scen_labels, fontsize=10)
ax2.set_ylim(0,1); ax2.set_ylabel('Predicted probability of suicidal ideation')
ax2.set_title('Model-predicted probability by risk profile (logistic regression)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/student_predicted_probability_scenarios.png', dpi=130, bbox_inches='tight')
print("Saved figure 2")

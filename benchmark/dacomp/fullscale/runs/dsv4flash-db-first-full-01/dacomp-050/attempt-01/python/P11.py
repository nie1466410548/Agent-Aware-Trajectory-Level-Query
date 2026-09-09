import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load(sid, cols):
    rows=[]
    with open(f'/results/S{sid}.rows.jsonl') as f:
        for line in f: rows.append(json.loads(line))
    return pd.DataFrame(rows, columns=cols)

# Grouped prevalence data from archived SQL queries
sleep_df = load(14, ['Sleep duration','total','yes_n','yes_pct'])
diet_df  = load(15, ['diet_group','total','yes_n','yes_pct']).iloc[:3].copy()
acad_df  = load(16, ['acad_group','total','yes_n','yes_pct'])
fin_df   = load(17, ['fin_group','total','yes_n','yes_pct'])
risk_df  = load(29, ['n_risk','total','yes_n','yes_pct'])

# Diet/sleep cross-tab from S25
ds_df = load(25, ['Dietary habits','sleep_cat','total','yes_n','yes_pct'])
ds_piv = ds_df.pivot(index='Dietary habits', columns='sleep_cat', values='yes_pct').reindex(['Healthy','Moderate','Unhealthy'])

order_acad = ['Low (1-2)','Medium (3)','High (4-5)']
order_fin = ['Low (1-2)','Medium (3)','High (4-5)']
order_diet = ['Healthy','Moderate','Unhealthy']
order_sleep = ['More than 8 hours','7-8 hours','5-6 hours','Less than 5 hours']

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

def bar(ax, labels, vals, title, color='#4C72B0', vline=None):
    bars = ax.bar(range(len(labels)), vals, color=color, edgecolor='black')
    for i,v in enumerate(vals): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=20, ha='right', fontsize=10)
    ax.set_ylabel('With suicidal thoughts (%)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100); ax.axhline(62.8, color='gray', ls='--', lw=1)
    ax.text(len(labels)-0.02, 64.5, 'overall 62.8%', color='gray', fontsize=9, ha='right')
    ax.grid(axis='y', alpha=0.3)

bar(axes[0,0], order_acad, acad_df.set_index('acad_group').loc[order_acad,'yes_pct'].values,
    'Academic stress', color='#C44E52')
bar(axes[0,1], order_fin, fin_df.set_index('fin_group').loc[order_fin,'yes_pct'].values,
    'Financial (economic) stress', color='#DD8452')
bar(axes[0,2], order_diet, diet_df.set_index('diet_group').loc[order_diet,'yes_pct'].values,
    'Dietary habits', color='#55A868')
bar(axes[1,0], order_sleep, sleep_df.set_index('Sleep duration').loc[order_sleep,'yes_pct'].values,
    'Sleep duration', color='#8172B3')

# Combined diet x sleep heatmap
im = axes[1,1].imshow(ds_piv.values, cmap='YlOrRd', vmin=50, vmax=80, aspect='auto')
axes[1,1].set_xticks(range(len(ds_piv.columns))); axes[1,1].set_xticklabels(ds_piv.columns, fontsize=10)
axes[1,1].set_yticks(range(len(ds_piv.index))); axes[1,1].set_yticklabels(ds_piv.index, fontsize=10)
for i in range(ds_piv.shape[0]):
    for j in range(ds_piv.shape[1]):
        axes[1,1].text(j, i, f"{ds_piv.values[i,j]:.1f}%", ha='center', va='center', fontsize=11, fontweight='bold')
axes[1,1].set_title('Diet × Sleep prevalence (%)', fontsize=12, fontweight='bold')
axes[1,1].set_xlabel('Sleep'); axes[1,1].set_ylabel('Diet')

# Risk factor dose-response
ax = axes[1,2]
vals = risk_df.set_index('n_risk').loc[[0,1,2,3,4],'yes_pct'].values
labels = ['0','1','2','3','4']
bars = ax.bar(range(5), vals, color='#C44E52', edgecolor='black')
for i,v in enumerate(vals): ax.text(i, v+1, f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
ax.set_xticks(range(5)); ax.set_xticklabels(labels)
ax.set_ylim(0,100); ax.grid(axis='y', alpha=0.3)
ax.set_ylabel('With suicidal thoughts (%)'); ax.set_xlabel('Number of risk factors')
ax.set_title('Dose–response: number of risk factors\n(academic≥4, financial≥4, unhealthy diet, sleep<5h)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/student_suicidal_ideation_characteristics.png', dpi=130, bbox_inches='tight')
print("Saved figure 1")

# Scenario predicted probability chart
scen_labels = ['Protective\n(low stress,\nhealthy)','High financial\nstress only','High academic\nstress only','High both\nstresses','High both +\nunhealthy diet\n+ <5h sleep']
scen_probs = [0.256, 0.584, 0.488, 0.848, 0.909]
fig2, ax2 = plt.subplots(figsize=(9,5))
bars = ax2.bar(range(len(scen_labels)), scen_probs, color=['#55A868','#DD8452','#4C72B0','#C44E52','#8B0000'], edgecolor='black')
for i,v in enumerate(scen_probs): ax2.text(i, v+0.01, f'{v*100:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax2.set_xticks(range(len(scen_labels))); ax2.set_xticklabels(scen_labels, fontsize=10)
ax2.set_ylim(0,1); ax2.set_ylabel('Predicted probability of suicidal ideation')
ax2.set_title('Model-predicted probability by risk profile (logistic regression)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/student_predicted_probability_scenarios.png', dpi=130, bbox_inches='tight')
print("Saved figure 2")

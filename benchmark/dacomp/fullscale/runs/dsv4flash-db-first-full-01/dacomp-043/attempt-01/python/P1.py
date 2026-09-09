import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ============= Figure 1: Symptoms - Complications by Outcome =============
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Complication type
complications = ['Skin Infection', 'Encephalitis', 'Pneumonia']
deceased_comp = [20, 15, 23]  # n=58
recovered_comp = [121, 67, 36]  # n=224
deceased_comp_pct = [c/58*100 for c in deceased_comp]
recovered_comp_pct = [c/224*100 for c in recovered_comp]
x = np.arange(len(complications))
width = 0.35
ax1 = axes[0, 0]
bars1 = ax1.bar(x - width/2, deceased_comp_pct, width, label='Deceased (n=58)', color='#d62728')
bars2 = ax1.bar(x + width/2, recovered_comp_pct, width, label='Recovered (n=224)', color='#2ca02c')
ax1.set_ylabel('Percentage of records (%)')
ax1.set_title('Complication Type Distribution')
ax1.set_xticks(x)
ax1.set_xticklabels(complications, fontsize=9)
ax1.legend()
ax1.set_ylim(0, 80)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 2. Associated Symptoms
symptoms = ['Cough', 'Headache', 'Vomiting']
deceased_symp = [14, 20, 24]
recovered_symp = [104, 42, 78]
deceased_symp_pct = [s/58*100 for s in deceased_symp]
recovered_symp_pct = [s/224*100 for s in recovered_symp]
ax2 = axes[0, 1]
bars1 = ax2.bar(x - width/2, deceased_symp_pct, width, label='Deceased', color='#d62728')
bars2 = ax2.bar(x + width/2, recovered_symp_pct, width, label='Recovered', color='#2ca02c')
ax2.set_ylabel('Percentage of records (%)')
ax2.set_title('Associated Symptoms Distribution')
ax2.set_xticks(x)
ax2.set_xticklabels(symptoms, fontsize=9)
ax2.legend()
ax2.set_ylim(0, 80)
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 3. Rash Distribution
rash_dists = ['Head & Face', 'Trunk', 'Limbs']
deceased_rash = [20, 16, 22]
recovered_rash = [67, 115, 42]
deceased_rash_pct = [r/58*100 for r in deceased_rash]
recovered_rash_pct = [r/224*100 for r in recovered_rash]
ax3 = axes[0, 2]
bars1 = ax3.bar(x - width/2, deceased_rash_pct, width, label='Deceased', color='#d62728')
bars2 = ax3.bar(x + width/2, recovered_rash_pct, width, label='Recovered', color='#2ca02c')
ax3.set_ylabel('Percentage of records (%)')
ax3.set_title('Rash Distribution')
ax3.set_xticks(x)
ax3.set_xticklabels(rash_dists, fontsize=9)
ax3.legend()
ax3.set_ylim(0, 70)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 4. Rash Morphology
morphs = ['Macule', 'Papule', 'Vesicle']
deceased_morph = [12, 17, 29]
recovered_morph = [76, 82, 66]
deceased_morph_pct = [m/58*100 for m in deceased_morph]
recovered_morph_pct = [m/224*100 for m in recovered_morph]
ax4 = axes[1, 0]
bars1 = ax4.bar(x - width/2, deceased_morph_pct, width, label='Deceased', color='#d62728')
bars2 = ax4.bar(x + width/2, recovered_morph_pct, width, label='Recovered', color='#2ca02c')
ax4.set_ylabel('Percentage of records (%)')
ax4.set_title('Rash Morphology')
ax4.set_xticks(x)
ax4.set_xticklabels(morphs, fontsize=9)
ax4.legend()
ax4.set_ylim(0, 70)
for bar in bars1:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 5. Treatment
treatments = ['Antiviral', 'Symptomatic']
deceased_trt = [24, 32]
recovered_trt = [94, 130]
deceased_trt_pct = [t/58*100 for t in deceased_trt]
recovered_trt_pct = [t/224*100 for t in recovered_trt]
ax5 = axes[1, 1]
x2 = np.arange(len(treatments))
bars1 = ax5.bar(x2 - width/2, deceased_trt_pct, width, label='Deceased', color='#d62728')
bars2 = ax5.bar(x2 + width/2, recovered_trt_pct, width, label='Recovered', color='#2ca02c')
ax5.set_ylabel('Percentage of records (%)')
ax5.set_title('Treatment Type')
ax5.set_xticks(x2)
ax5.set_xticklabels(treatments, fontsize=9)
ax5.legend()
ax5.set_ylim(0, 80)
for bar in bars1:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 6. Hospitalization
hosp_labels = ['Hospitalized', 'Not Hospitalized']
deceased_hosp = [27, 29]
recovered_hosp = [92, 132]
deceased_hosp_pct = [h/58*100 for h in deceased_hosp]
recovered_hosp_pct = [h/224*100 for h in recovered_hosp]
ax6 = axes[1, 2]
x3 = np.arange(len(hosp_labels))
bars1 = ax6.bar(x3 - width/2, deceased_hosp_pct, width, label='Deceased', color='#d62728')
bars2 = ax6.bar(x3 + width/2, recovered_hosp_pct, width, label='Recovered', color='#2ca02c')
ax6.set_ylabel('Percentage of records (%)')
ax6.set_title('Hospitalization Status')
ax6.set_xticks(x3)
ax6.set_xticklabels(hosp_labels, fontsize=9)
ax6.legend()
ax6.set_ylim(0, 80)
for bar in bars1:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

plt.suptitle('HFMD: Deceased vs Recovered Population — Symptoms & Treatment Comparison', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/work/figure1_symptoms_treatment.png', dpi=150, bbox_inches='tight')
plt.close()

# ============= Figure 2: Prevention/Control and Diagnosis =============
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Isolation Status
iso_labels = ['Isolated', 'Not Isolated']
deceased_iso = [35, 21]
recovered_iso = [100, 124]
deceased_iso_pct = [i/58*100 for i in deceased_iso]
recovered_iso_pct = [i/224*100 for i in recovered_iso]
ax1 = axes[0, 0]
x2 = np.arange(len(iso_labels))
bars1 = ax1.bar(x2 - width/2, deceased_iso_pct, width, label='Deceased', color='#d62728')
bars2 = ax1.bar(x2 + width/2, recovered_iso_pct, width, label='Recovered', color='#2ca02c')
ax1.set_ylabel('Percentage (%)')
ax1.set_title('Isolation Status')
ax1.set_xticks(x2)
ax1.set_xticklabels(iso_labels, fontsize=9)
ax1.legend()
ax1.set_ylim(0, 80)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 2. PPE Usage during Isolation
ppe_labels = ['Complete PPE', 'Missing PPE']
deceased_ppe = [9, 6]
recovered_ppe = [66, 29]
deceased_ppe_pct = [p/15*100 for p in deceased_ppe]  # 15 total isolation records for deceased
recovered_ppe_pct = [p/95*100 for p in recovered_ppe]  # 95 total isolation records for recovered
ax2 = axes[0, 1]
bars1 = ax2.bar(x2 - width/2, deceased_ppe_pct, width, label='Deceased', color='#d62728')
bars2 = ax2.bar(x2 + width/2, recovered_ppe_pct, width, label='Recovered', color='#2ca02c')
ax2.set_ylabel('Percentage (%)')
ax2.set_title('PPE Usage During Isolation')
ax2.set_xticks(x2)
ax2.set_xticklabels(ppe_labels, fontsize=9)
ax2.legend()
ax2.set_ylim(0, 100)
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 3. Diagnostic Quality Score
metrics = ['Avg Quality Score', 'Avg Compliance Rate']
deceased_qual = [53.37, 0.56]
recovered_qual = [69.30, 0.75]
ax3 = axes[0, 2]
x3 = np.arange(len(metrics))
# Scale compliance for display
deceased_qual_scaled = [53.37, 0.56*100]
recovered_qual_scaled = [69.30, 0.75*100]
bars1 = ax3.bar(x3 - width/2, deceased_qual_scaled, width, label='Deceased', color='#d62728')
bars2 = ax3.bar(x3 + width/2, recovered_qual_scaled, width, label='Recovered', color='#2ca02c')
ax3.set_ylabel('Score (0-100)')
ax3.set_title('Diagnostic Quality')
ax3.set_xticks(x3)
ax3.set_xticklabels(metrics, fontsize=9)
ax3.legend()
ax3.set_ylim(0, 100)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.1f}', ha='center', fontsize=8)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.1f}', ha='center', fontsize=8)

# 4. Initial Diagnosis
init_diag = ['Suspected', 'Clinical', 'Confirmed']
deceased_diag = [7, 14, 5]
recovered_diag = [96, 24, 52]
deceased_diag_pct = [d/26*100 for d in deceased_diag]
recovered_diag_pct = [d/172*100 for d in recovered_diag]
ax4 = axes[1, 0]
bars1 = ax4.bar(x - width/2, deceased_diag_pct, width, label='Deceased', color='#d62728')
bars2 = ax4.bar(x + width/2, recovered_diag_pct, width, label='Recovered', color='#2ca02c')
ax4.set_ylabel('Percentage (%)')
ax4.set_title('Initial Diagnosis Type')
ax4.set_xticks(x)
ax4.set_xticklabels(init_diag, fontsize=9)
ax4.legend()
ax4.set_ylim(0, 70)
for bar in bars1:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 5. Diagnostic Delay
delay_labels = ['No Delay', 'Patient Delayed']
deceased_delay = [10, 16]
recovered_delay = [115, 57]
deceased_delay_pct = [d/26*100 for d in deceased_delay]
recovered_delay_pct = [d/172*100 for d in recovered_delay]
ax5 = axes[1, 1]
bars1 = ax5.bar(x2 - width/2, deceased_delay_pct, width, label='Deceased', color='#d62728')
bars2 = ax5.bar(x2 + width/2, recovered_delay_pct, width, label='Recovered', color='#2ca02c')
ax5.set_ylabel('Percentage (%)')
ax5.set_title('Diagnostic Delay')
ax5.set_xticks(x2)
ax5.set_xticklabels(delay_labels, fontsize=9)
ax5.legend()
ax5.set_ylim(0, 80)
for bar in bars1:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax5.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 6. Medical Insurance Reimbursement
reimb_labels = ['Deceased', 'Recovered']
reimb_values = [3.35, 58.64]
ax6 = axes[1, 2]
bars = ax6.bar(reimb_labels, reimb_values, color=['#d62728', '#2ca02c'], width=0.5)
ax6.set_ylabel('Average Reimbursement (%)')
ax6.set_title('Medical Insurance Reimbursement\n(Complication Treatment)')
for bar in bars:
    ax6.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5, f'{bar.get_height():.2f}%', ha='center', fontsize=10)

plt.suptitle('HFMD: Deceased vs Recovered Population — Prevention, Control & Diagnosis Comparison', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/work/figure2_prevention_control_diagnosis.png', dpi=150, bbox_inches='tight')
plt.close()

print("Figures created successfully.")
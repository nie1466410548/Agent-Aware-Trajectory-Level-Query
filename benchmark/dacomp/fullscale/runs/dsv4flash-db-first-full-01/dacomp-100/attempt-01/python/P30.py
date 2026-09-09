import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Milestone by outcome (manually from SQL results)
milestones = ['Usage Insights Published', 'Security Audit Passed', 'Support Automation Live', 
              'ROI Review Delivered', 'Invoice Automation Live',
              'Data Warehouse Sync Completed',
              'Customer Journey Dashboard Launched', 'Mobile Rollout Completed',
              'Role-based Access Rolled Out', 'Billing Integration Completed']
renewed_m = [251, 250, 251, 84, 83, 0, 0, 0, 0, 0]
churned_m = [0, 0, 0, 0, 0, 0, 251, 251, 251, 251]
monitor_m = [0, 0, 0, 167, 168, 251, 0, 0, 0, 0]

plt.figure(figsize=(14, 6))
x = np.arange(len(milestones))
width = 0.25

plt.bar(x - width, renewed_m, width, label='Renewed (Upsell Ready)', color='#27ae60')
plt.bar(x, churned_m, width, label='Churned (Risk Mitigation)', color='#e74c3c')
plt.bar(x + width, monitor_m, width, label='Monitor', color='#f39c12')

plt.xticks(x, milestones, rotation=45, ha='right', fontsize=9)
plt.ylabel('Number of Companies', fontsize=12)
plt.title('Last Value Milestone vs Renewal Outcome', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('milestone_outcome.png', dpi=100)
print("Saved: milestone_outcome.png")

# Education focus by outcome
edu_labels = ['AI Enablement', 'Data Quality', 'Governance', 'Adoption', 'Analytics', 'Onboarding',
              'Billing Automation', 'Integration', 'Security', 'Workflow Automation']
renewed_e = [250, 251, 251, 84, 0, 83, 0, 0, 0, 0]
churned_e = [0, 0, 0, 0, 0, 0, 251, 251, 251, 251]
monitor_e = [0, 0, 0, 167, 251, 168, 0, 0, 0, 0]

plt.figure(figsize=(14, 6))
x = np.arange(len(edu_labels))
plt.bar(x - width, renewed_e, width, label='Renewed (Upsell Ready)', color='#27ae60')
plt.bar(x, churned_e, width, label='Churned (Risk Mitigation)', color='#e74c3c')
plt.bar(x + width, monitor_e, width, label='Monitor', color='#f39c12')

plt.xticks(x, edu_labels, rotation=45, ha='right', fontsize=9)
plt.ylabel('Number of Companies', fontsize=12)
plt.title('Education Focus vs Renewal Outcome', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('education_outcome.png', dpi=100)
print("Saved: education_outcome.png")
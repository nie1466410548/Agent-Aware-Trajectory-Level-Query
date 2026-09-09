import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_pickle('/work/analysis_data.pkl')
df['active_share'] = 1 - df['days_since_last_activity'] / df['account_age_days'].clip(lower=1)
hve = df[df['customer_group']=='HVE'].copy()

segments = ['Champion', 'Potential Loyalist', 'Loyal Customer', 'At Risk']
profile_data = []
for seg in segments:
    sub = hve[hve['customer_segment']==seg]
    if len(sub) == 0:
        continue
    profile_data.append({
        'Segment': seg,
        'Count': len(sub),
        'Avg LTV': sub['estimated_customer_ltv'].mean(),
        'Health Score': sub['customer_health_score'].mean(),
        'Churn Prob': sub['churn_probability'].mean(),
        'Recency (R)': sub['recency_score'].mean(),
        'Frequency (F)': sub['frequency_score'].mean(),
        'Monetary (M)': sub['monetary_score'].mean(),
        'M-RF Gap': sub['m_rf_gap'].mean(),
        'Active Share': sub['active_share'].mean(),
        'Account Age': sub['account_age_days'].mean(),
        'Inactive Days': sub['days_since_last_activity'].mean(),
    })
prof = pd.DataFrame(profile_data).set_index('Segment')

# Manual min-max normalization (0 to 1)
prof_norm = (prof - prof.min()) / (prof.max() - prof.min())

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(prof_norm, annot=prof.round(1), fmt='.1f', cmap='RdYlGn', 
            linewidths=1, ax=ax, cbar_kws={'label': 'Normalized Score (0=low, 1=high)'})
ax.set_title('HVE Segment Profile Comparison (Normalized)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/fig10_hve_profiles.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig10 saved")

# FIGURE 11: Strategy Quadrant
fig, ax = plt.subplots(figsize=(10, 7))
colors = {'Champion': '#2ECC71', 'Loyal Customer': '#3498DB', 'Potential Loyalist': '#F39C12', 'At Risk': '#E74C3C'}
for seg in segments:
    sub = hve[hve['customer_segment']==seg]
    ax.scatter(sub['composite_rfm'], sub['churn_probability'], 
               c=colors.get(seg, '#95A5A6'), label=seg, s=sub['estimated_customer_ltv']/200, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.axvline(x=4.0, color='gray', linestyle='--', alpha=0.5)
ax.axhline(y=0.4, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Composite RFM Score (Value)', fontsize=12)
ax.set_ylabel('Churn Probability (Risk)', fontsize=12)
ax.set_title('HVE Strategy Quadrant: Value vs Risk\n(Bubble size = LTV)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='lower right')
plt.tight_layout()
plt.savefig('/work/fig11_strategy_quadrant.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig11 saved")

# FIGURE 12: Lifecycle stacked bar
fig, ax = plt.subplots(figsize=(12, 5))
lifecycle_order = ['Activation', 'Growth', 'Maturity', 'Retention', 'Dormant']
data = pd.crosstab(hve['customer_segment'], hve['lifecycle_stage'])[lifecycle_order]
data_pct = data.div(data.sum(axis=1), axis=0)
data_pct.plot(kind='bar', stacked=True, ax=ax, 
              color=['#2ECC71','#F39C12','#9B59B6','#E74C3C','#95A5A6'])
ax.set_title('Lifecycle Stage Distribution within HVE Sub-Segments', fontsize=14, fontweight='bold')
ax.set_xlabel('HVE Customer Segment', fontsize=12)
ax.set_ylabel('Proportion', fontsize=12)
ax.legend(title='Lifecycle Stage', fontsize=9)
ax.set_xticklabels(segments, rotation=0)
plt.tight_layout()
plt.savefig('/work/fig12_hve_lifecycle.png', dpi=150, bbox_inches='tight')
plt.close()
print("Fig12 saved")

print("All strategy figures saved!")
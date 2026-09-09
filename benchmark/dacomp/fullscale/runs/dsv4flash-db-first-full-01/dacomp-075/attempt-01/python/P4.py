import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df = pd.read_csv('/work/focus_group_with_scores.csv')
df['contract_expiry_date'] = pd.to_datetime(df['contract_expiry_date'])
df['analysis_date'] = pd.to_datetime(df['analysis_date'])
df['days_until_contract_expiry'] = (df['contract_expiry_date'] - df['analysis_date']).dt.days

# Reference analysis date = 2024-01-01 (earliest), use it as planning baseline
# Risk window: next 12-18 months from baseline
baseline = pd.Timestamp('2024-01-01')

# ==========================================
# DYNAMIC RISK WARNING MECHANISM
# ==========================================

# RISK INDICATORS (all normalized 0-100, higher = more risk)

# 1. Contract Expiry Risk: contract expiring within 12-18 months
#    Expiry within next 12 months = very high risk, 12-18 = high
days_to_expiry = df['days_until_contract_expiry'].clip(lower=0)
df['contract_expiry_risk'] = np.where(days_to_expiry <= 365, 100,
                             np.where(days_to_expiry <= 550, 80,
                             np.where(days_to_expiry <= 730, 60,
                             np.where(days_to_expiry <= 900, 40, 20))))

# 2. Financial Distress Risk: low financial health, high overdue
fin_health = df['financial_health_score'].values
df['fin_distress_risk'] = ((100 - df['financial_health_score_norm']) * 0.5 + 
                           (100 - df['financial_overdue_score']) * 0.3 +
                           (100 - df['financial_delay_score']) * 0.2)

# 3. Operational Weakness Risk
df['operational_weakness_risk'] = 100 - df['operational_resilience']

# 4. Market Risk: high volatility, few alternatives, high price volatility, high switching cost
df['market_risk'] = 100 - df['market_resilience']

# 5. Inactivity Risk: days since last transaction
df['inactivity_risk'] = np.where(df['days_since_last_transaction'] > 90, 100,
                         np.where(df['days_since_last_transaction'] > 60, 80,
                         np.where(df['days_since_last_transaction'] > 30, 60,
                         np.where(df['days_since_last_transaction'] > 14, 40, 20))))

# 6. Concentration Risk: high spend concentration = high dependence
df['concentration_risk'] = df['spend_concentration_ratio'] * 100

# 7. Dependency Risk: categorical dependency level
dep_map = {'Critical': 100, 'High': 80, 'High Dependency': 70, 'Medium Dependency': 50, 
           'Low Dependency': 30, 'Minimal Dependency': 10}
df['dependency_risk'] = df['dependency_level'].map(dep_map).fillna(50)

# 8. Dormancy Risk: activity status
act_map = {'Dormant': 100, 'Inactive': 70, 'Moderate': 40, 'Active': 10}
df['activity_risk'] = df['activity_status'].map(act_map).fillna(50)

# ==========================================
# COMPOSITE DISRUPTION PROBABILITY SCORE
# (12-18 month horizon)
# ==========================================
# Weights: financial distress and dependency are most predictive of disruption
df['disruption_probability_12_18mo'] = (
    0.20 * df['fin_distress_risk'] + 
    0.15 * df['dependency_risk'] + 
    0.15 * df['activity_risk'] + 
    0.12 * df['contract_expiry_risk'] + 
    0.12 * df['operational_weakness_risk'] + 
    0.12 * df['market_risk'] + 
    0.09 * df['concentration_risk'] + 
    0.05 * df['inactivity_risk']
)

# Warning levels
def warn_level(prob):
    if prob >= 75: return 'RED ALERT - Critical Disruption Risk'
    elif prob >= 60: return 'AMBER - High Disruption Risk'
    elif prob >= 45: return 'YELLOW - Elevated Disruption Risk'
    else: return 'GREEN - Monitor'

df['warning_level'] = df['disruption_probability_12_18mo'].apply(warn_level)

print("=== DISRUPTION RISK WARNING DISTRIBUTION ===")
print(df['warning_level'].value_counts())
print(f"\nDisruption Probability: Mean={df['disruption_probability_12_18mo'].mean():.1f}, "
      f"Median={df['disruption_probability_12_18mo'].median():.1f}, "
      f"Max={df['disruption_probability_12_18mo'].max():.1f}")

# ==========================================
# IDENTIFY HIGH-RISK SCENARIOS
# ==========================================
# High-risk scenarios: disruption probability >= 60 AND high business impact
high_risk = df[df['disruption_probability_12_18mo'] >= 60].sort_values('disruption_probability_12_18mo', ascending=False)
print(f"\n=== HIGH-RISK VENDORS (Disruption Prob >= 60) - {len(high_risk)} vendors ===")
for _, r in high_risk.iterrows():
    print(f"{r['vendor_name'][:35]:37s} | Prob={r['disruption_probability_12_18mo']:.0f} | {r['warning_level'][:12]} | Spend=${r['total_vendor_spend']:>9,.0f} | OverallRes={r['overall_resilience']:.0f}")

# Save
df.to_csv('/work/risk_warning_results.csv', index=False)
high_risk.to_csv('/work/high_risk_vendors.csv', index=False)

# ==========================================
# FIGURE 6: Disruption probability distribution
# ==========================================
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Left: histogram of disruption probability
axes[0].hist(df['disruption_probability_12_18mo'], bins=20, color='#e74c3c', 
             edgecolor='white', alpha=0.8)
axes[0].axvline(75, color='red', linestyle='--', label='Critical (75+)')
axes[0].axvline(60, color='orange', linestyle='--', label='High (60+)')
axes[0].axvline(45, color='yellow', linestyle='--', label='Elevated (45+)')
axes[0].set_xlabel('12-18 Month Disruption Probability Score')
axes[0].set_ylabel('Number of Vendors')
axes[0].set_title('Disruption Risk Distribution', fontsize=14, fontweight='bold')
axes[0].legend()

# Middle: warning level distribution
warning_counts = df['warning_level'].value_counts()
colors_map = {'RED ALERT - Critical Disruption Risk': '#c0392b',
              'AMBER - High Disruption Risk': '#e67e22',
              'YELLOW - Elevated Disruption Risk': '#f1c40f',
              'GREEN - Monitor': '#27ae60'}
axes[1].bar(range(len(warning_counts)), warning_counts.values, 
            color=[colors_map.get(l, '#95a5a6') for l in warning_counts.index])
axes[1].set_xticks(range(len(warning_counts)))
axes[1].set_xticklabels([l[:6] for l in warning_counts.index], rotation=0)
axes[1].set_xlabel('Warning Level')
axes[1].set_ylabel('Number of Vendors')
axes[1].set_title('Warning Level Distribution', fontsize=14, fontweight='bold')
for i, v in enumerate(warning_counts.values):
    axes[1].text(i, v+0.5, str(v), ha='center', fontweight='bold')

# Right: risk score vs resilience bubble chart
scatter = axes[2].scatter(df['overall_resilience'], df['disruption_probability_12_18mo'],
                          s=df['total_vendor_spend']/20000, c=df['vendor_risk_score'],
                          cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=0.5)
axes[2].set_xlabel('Overall Resilience Score')
axes[2].set_ylabel('Disruption Probability (12-18mo)')
axes[2].set_title('Resilience vs Disruption Risk\n(Bubble = Spend)', fontsize=14, fontweight='bold')
axes[2].axhline(60, color='red', linestyle='--', alpha=0.5)
axes[2].axvline(50, color='blue', linestyle='--', alpha=0.5)
cbar = plt.colorbar(scatter, ax=axes[2])
cbar.set_label('Risk Score')

plt.tight_layout()
plt.savefig('/work/figure6_disruption_risk.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigure 6 saved")
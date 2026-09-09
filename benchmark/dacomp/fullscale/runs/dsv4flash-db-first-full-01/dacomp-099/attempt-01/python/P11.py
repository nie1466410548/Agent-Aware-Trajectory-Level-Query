import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load the plan-period analysis
evdf = pd.read_csv('/work/plan_period_analysis.csv')
evdf['event_at'] = pd.to_datetime(evdf['event_at'])

print("=== Between-group comparison (upgrade vs downgrade) ===")
up = evdf[evdf['event_type']=='upgrade']
dn = evdf[evdf['event_type']=='downgrade']

# Compare before-period metrics
print("\n--- Before-period metrics ---")
for col, label in [('before_conv_rate', 'Conversation rate'), ('before_bug_rate', 'Bug rate'),
                   ('before_outage_rate', 'Outage rate'), ('before_sla_rate', 'SLA breach rate')]:
    t, p = stats.ttest_ind(up[col].values, dn[col].values, equal_var=False)
    print(f"  {label}: upgrade={up[col].mean():.4f}, downgrade={dn[col].mean():.4f}, t={t:.3f}, p={p:.4f}")

print("\n--- After-period metrics ---")
for col, label in [('after_conv_rate', 'Conversation rate'), ('after_bug_rate', 'Bug rate'),
                   ('after_outage_rate', 'Outage rate'), ('after_sla_rate', 'SLA breach rate')]:
    t, p = stats.ttest_ind(up[col].values, dn[col].values, equal_var=False)
    print(f"  {label}: upgrade={up[col].mean():.4f}, downgrade={dn[col].mean():.4f}, t={t:.3f}, p={p:.4f}")

print("\n--- Delta (after - before) metrics ---")
for col, label in [('after_conv_rate', 'Conv rate'), ('after_bug_rate', 'Bug rate'),
                   ('after_outage_rate', 'Outage rate'), ('after_sla_rate', 'SLA breach rate')]:
    up_delta = (up[col] - up[col.replace('after_', 'before_')]).values
    dn_delta = (dn[col] - dn[col.replace('after_', 'before_')]).values
    t, p = stats.ttest_ind(up_delta, dn_delta, equal_var=False)
    print(f"  {label} delta: upgrade={up_delta.mean():.4f}, downgrade={dn_delta.mean():.4f}, t={t:.3f}, p={p:.4f}")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Before vs After conversation rates by event type
ax = axes[0,0]
for i, evt in enumerate(['upgrade', 'downgrade']):
    sub = evdf[evdf['event_type'] == evt]
    ax.scatter(sub['before_conv_rate'], sub['after_conv_rate'], label=f'{evt} (n={len(sub)})', alpha=0.7, s=60)
ax.plot([0, 5], [0, 5], 'k--', alpha=0.3)
ax.set_xlabel('Before: Conversation Rate (per day)')
ax.set_ylabel('After: Conversation Rate (per day)')
ax.set_title('Conversation Rate Before vs After Plan Change')
ax.legend()
ax.grid(alpha=0.3)

# Plot 2: Bug rate before vs after
ax = axes[0,1]
for i, evt in enumerate(['upgrade', 'downgrade']):
    sub = evdf[evdf['event_type'] == evt]
    ax.scatter(sub['before_bug_rate'], sub['after_bug_rate'], label=f'{evt} (n={len(sub)})', alpha=0.7, s=60)
ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
ax.set_xlabel('Before: Bug Rate (per day)')
ax.set_ylabel('After: Bug Rate (per day)')
ax.set_title('Bug Rate Before vs After Plan Change')
ax.legend()
ax.grid(alpha=0.3)

# Plot 3: Bar chart of before metrics comparison
ax = axes[1,0]
metrics = ['conv_rate', 'bug_rate', 'outage_rate', 'sla_rate']
labels = ['Conversation Rate', 'Bug Rate', 'Outage Rate', 'SLA Breach Rate']
x = np.arange(len(metrics))
width = 0.35
up_means = [up[f'before_{m}'].mean() for m in metrics]
dn_means = [dn[f'before_{m}'].mean() for m in metrics]
bars1 = ax.bar(x - width/2, up_means, width, label='Upgrade', alpha=0.8)
bars2 = ax.bar(x + width/2, dn_means, width, label='Downgrade', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_ylabel('Rate (per day)')
ax.set_title('Before-Event Metrics Comparison')
ax.legend()
ax.grid(alpha=0.3, axis='y')

# Plot 4: Bar chart of deltas
ax = axes[1,1]
up_deltas = [up[f'after_{m}'].mean() - up[f'before_{m}'].mean() for m in metrics]
dn_deltas = [dn[f'after_{m}'].mean() - dn[f'before_{m}'].mean() for m in metrics]
bars1 = ax.bar(x - width/2, up_deltas, width, label='Upgrade', alpha=0.8)
bars2 = ax.bar(x + width/2, dn_deltas, width, label='Downgrade', alpha=0.8)
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_ylabel('Delta (After - Before)')
ax.set_title('Change in Metrics After Plan Change')
ax.legend()
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/work/plan_change_analysis.png', dpi=150)
print("\nSaved figure to /work/plan_change_analysis.png")

# Additional analysis: What specific factors correlate with upgrades vs downgrades?
# Let's look at the company metrics from the company_metrics table
metrics_sql = """
SELECT ce.company_name, ce.plan_name, ce.monthly_spend, cm.*
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id
"""
company_data = db.frame(db.query(metrics_sql))
print("\nCompany metrics shape:", company_data.shape)

# Get the latest snapshot per company (by updated_at)
company_data = company_data.sort_values('updated_at', ascending=False).drop_duplicates('company_name')
print("After dedup:", company_data.shape)

# Merge with event data - get the PRE-CHANGE snapshot for each event
evdf_merged = evdf.merge(company_data, on='company_name', how='left')
print("Merged with company data:", evdf_merged.shape)

# Compare metrics between upgrade and downgrade events
print("\n=== Company characteristics comparison ===")
for col in ['monthly_spend', 'user_count', 'session_count', 'total_conversations', 
            'avg_conversation_rating', 'p50_time_to_first_response_min', 'p50_reopens',
            'registration_retention_7d', 'registration_retention_30d']:
    up_vals = evdf_merged[evdf_merged['event_type']=='upgrade'][col].dropna()
    dn_vals = evdf_merged[evdf_merged['event_type']=='downgrade'][col].dropna()
    if len(up_vals) > 1 and len(dn_vals) > 1:
        t, p = stats.ttest_ind(up_vals, dn_vals, equal_var=False)
        print(f"  {col}: upgrade={up_vals.mean():.2f}, downgrade={dn_vals.mean():.2f}, t={t:.3f}, p={p:.4f}")

plt.close('all')
print("\nDone.")
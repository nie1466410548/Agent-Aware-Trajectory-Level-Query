import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load the plan-period analysis
evdf = pd.read_csv('/work/plan_period_analysis.csv')
up = evdf[evdf['event_type']=='upgrade']
dn = evdf[evdf['event_type']=='downgrade']

# Figure 2: Event timeline with per-company rates before/after
fig, axes = plt.subplots(2, 3, figsize=(16, 9))

# Row 1: Conversation rate before vs after (connected lines per event)
ax = axes[0,0]
for evt, color in [('upgrade', 'tab:blue'), ('downgrade', 'tab:red')]:
    sub = evdf[evdf['event_type']==evt]
    x = np.arange(len(sub))
    ax.plot(x, sub['before_conv_rate'].values, 'o-', color=color, alpha=0.4, label=f'{evt} before')
    ax.plot(x, sub['after_conv_rate'].values, 's--', color=color, alpha=0.6, label=f'{evt} after')
ax.set_xlabel('Event (index)')
ax.set_ylabel('Conversation rate (per day)')
ax.set_title('Conversation Rate: Before vs After (per event)')
ax.legend(fontsize=7, ncol=2)
ax.grid(alpha=0.3)

# Row 1 col 2: Bug rate
ax = axes[0,1]
for evt, color in [('upgrade', 'tab:blue'), ('downgrade', 'tab:red')]:
    sub = evdf[evdf['event_type']==evt]
    x = np.arange(len(sub))
    ax.plot(x, sub['before_bug_rate'].values, 'o-', color=color, alpha=0.4)
    ax.plot(x, sub['after_bug_rate'].values, 's--', color=color, alpha=0.6)
ax.set_xlabel('Event (index)')
ax.set_ylabel('Bug rate (per day)')
ax.set_title('Bug Rate: Before vs After (per event)')
ax.grid(alpha=0.3)

# Row 1 col 3: SLA breach rate
ax = axes[0,2]
for evt, color in [('upgrade', 'tab:blue'), ('downgrade', 'tab:red')]:
    sub = evdf[evdf['event_type']==evt]
    x = np.arange(len(sub))
    ax.plot(x, sub['before_sla_rate'].values, 'o-', color=color, alpha=0.4, label=f'{evt} before')
    ax.plot(x, sub['after_sla_rate'].values, 's--', color=color, alpha=0.6, label=f'{evt} after')
ax.set_xlabel('Event (index)')
ax.set_ylabel('SLA breach rate (per day)')
ax.set_title('SLA Breach Rate: Before vs After')
ax.legend(fontsize=7, ncol=2)
ax.grid(alpha=0.3)

# Row 2: Aggregated means comparison
ax = axes[1,0]
metrics = ['conv_rate', 'bug_rate', 'outage_rate', 'sla_rate']
labels = ['Conv.\nRate', 'Bug\nRate', 'Outage\nRate', 'SLA\nBreach']
x = np.arange(len(metrics))
width = 0.18
up_b = [up[f'before_{m}'].mean() for m in metrics]
up_a = [up[f'after_{m}'].mean() for m in metrics]
dn_b = [dn[f'before_{m}'].mean() for m in metrics]
dn_a = [dn[f'after_{m}'].mean() for m in metrics]
ax.bar(x - 1.5*width, up_b, width, label='Upgrade: before', color='tab:blue', alpha=0.6)
ax.bar(x - 0.5*width, up_a, width, label='Upgrade: after', color='tab:blue', alpha=1.0)
ax.bar(x + 0.5*width, dn_b, width, label='Downgrade: before', color='tab:red', alpha=0.6)
ax.bar(x + 1.5*width, dn_a, width, label='Downgrade: after', color='tab:red', alpha=1.0)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Rate (per day)')
ax.set_title('Usage & Incident Intensity: Before/After')
ax.legend(fontsize=7)
ax.grid(alpha=0.3, axis='y')

# Row 2 col 2: pre-event incident volume comparison (absolute)
ax = axes[1,1]
vol_metrics = ['before_bugs', 'before_outages', 'before_sla', 'before_escalations']
vol_labels = ['Bugs', 'Outages', 'SLA\nBreaches', 'Escalations']
# Normalize to per-100-days for fair comparison
up_vol = [up[m].sum() / up['before_days'].sum() * 100 for m in vol_metrics]
dn_vol = [dn[m].sum() / dn['before_days'].sum() * 100 for m in vol_metrics]
x = np.arange(len(vol_metrics))
ax.bar(x - width/2, up_vol, width, label='Upgrade (before)', color='tab:blue', alpha=0.8)
ax.bar(x + width/2, dn_vol, width, label='Downgrade (before)', color='tab:red', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(vol_labels)
ax.set_ylabel('Incidents per 100 days')
ax.set_title('Pre-Event Incident Volume (per 100 days)')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

# Row 2 col 3: Percent change in rates after event
ax = axes[1,2]
changes = {}
for m in metrics:
    up_c = (up[f'after_{m}'].mean() / up[f'before_{m}'].mean() - 1) * 100 if up[f'before_{m}'].mean() > 0 else np.nan
    dn_c = (dn[f'after_{m}'].mean() / dn[f'before_{m}'].mean() - 1) * 100 if dn[f'before_{m}'].mean() > 0 else np.nan
    changes[m] = (up_c, dn_c)
x = np.arange(len(metrics))
up_vals = [changes[m][0] for m in metrics]
dn_vals = [changes[m][1] for m in metrics]
ax.bar(x - width/2, up_vals, width, label='Upgrade', color='tab:blue', alpha=0.8)
ax.bar(x + width/2, dn_vals, width, label='Downgrade', color='tab:red', alpha=0.8)
ax.axhline(0, color='k', lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('% Change after event')
ax.set_title('% Change in Rate After Event')
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/work/plan_change_summary.png', dpi=150)
print("Saved /work/plan_change_summary.png")

# Table of paired test results for the report
print("\n=== Key statistics for report ===")
print("UPGRADE events:")
print(f"  n={len(up)}")
print(f"  conv rate: {up['before_conv_rate'].mean():.3f} -> {up['after_conv_rate'].mean():.3f} (p={stats.ttest_rel(up['after_conv_rate'], up['before_conv_rate'])[1]:.4f})")
print(f"  bug rate: {up['before_bug_rate'].mean():.3f} -> {up['after_bug_rate'].mean():.3f} (p={stats.ttest_rel(up['after_bug_rate'], up['before_bug_rate'])[1]:.4f})")
print(f"  outage rate: {up['before_outage_rate'].mean():.3f} -> {up['after_outage_rate'].mean():.3f}")
print(f"  SLA rate: {up['before_sla_rate'].mean():.3f} -> {up['after_sla_rate'].mean():.3f}")
print("\nDOWNGRADE events:")
print(f"  n={len(dn)}")
print(f"  conv rate: {dn['before_conv_rate'].mean():.3f} -> {dn['after_conv_rate'].mean():.3f} (p={stats.ttest_rel(dn['after_conv_rate'], dn['before_conv_rate'])[1]:.4f})")
print(f"  bug rate: {dn['before_bug_rate'].mean():.3f} -> {dn['after_bug_rate'].mean():.3f}")
print(f"  outage rate: {dn['before_outage_rate'].mean():.3f} -> {dn['after_outage_rate'].mean():.3f}")
print(f"  SLA rate: {dn['before_sla_rate'].mean():.3f} -> {dn['after_sla_rate'].mean():.3f}")

# Compare pre-event between groups
print("\nPre-event comparison (upgrade vs downgrade):")
for m, label in [('conv_rate','Conversation rate'), ('bug_rate','Bug rate'), ('sla_rate','SLA breach rate')]:
    t, p = stats.ttest_ind(up[f'before_{m}'].values, dn[f'before_{m}'].values, equal_var=False)
    print(f"  {label}: upgrade={up[f'before_{m}'].mean():.3f}, downgrade={dn[f'before_{m}'].mean():.3f}, p={p:.4f}")
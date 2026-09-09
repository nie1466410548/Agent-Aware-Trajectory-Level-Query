# Create a unique event identifier
df['event_key'] = df['company_name'] + '_' + df['event_at'].astype(str)

# Per-event, per-period aggregation
agg_cols = {
    'conversation_id': 'count',  # conversation count
    'count_total_parts': 'sum',  # total parts
    'is_bug': 'sum',
    'is_outage': 'sum',
    'is_escalation': 'sum',
    'is_renewal': 'sum',
    'is_sla_breach': 'sum',
    'is_customer_initiated': 'sum',
    'conversation_rating': lambda x: x[x > 0].mean() if (x > 0).any() else 0
}

per_event = df.groupby(['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan', 'period']).agg(agg_cols).reset_index()
per_event.columns = ['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan', 'period', 'conv_count', 'total_parts', 'bug_count', 'outage_count', 'escalation_count', 'renewal_count', 'sla_breach_count', 'customer_initiated_count', 'avg_rating']

# Pivot to have before/after as columns
pivot = per_event.pivot_table(index=['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan'],
                              columns='period', 
                              values=['conv_count', 'total_parts', 'bug_count', 'outage_count', 'escalation_count', 'renewal_count', 'sla_breach_count', 'customer_initiated_count', 'avg_rating'],
                              aggfunc='first').fillna(0)

# Flatten column names
pivot.columns = [f'{col[1]}_{col[0]}' for col in pivot.columns]
pivot = pivot.reset_index()

# Calculate deltas (after - before)
pivot['conv_delta'] = pivot['after_conv_count'] - pivot['before_conv_count']
pivot['parts_delta'] = pivot['after_total_parts'] - pivot['before_total_parts']
pivot['bug_delta'] = pivot['after_bug_count'] - pivot['before_bug_count']
pivot['outage_delta'] = pivot['after_outage_count'] - pivot['before_outage_count']
pivot['escalation_delta'] = pivot['after_escalation_count'] - pivot['before_escalation_count']
pivot['sla_breach_delta'] = pivot['after_sla_breach_count'] - pivot['before_sla_breach_count']

# Also compute relative change for conversations (normalized by before)
pivot['conv_change_pct'] = np.where(pivot['before_conv_count'] > 0, 
                                     (pivot['after_conv_count'] - pivot['before_conv_count']) / pivot['before_conv_count'] * 100,
                                     np.where(pivot['after_conv_count'] > 0, 100, 0))

print("=== Per-event summary ===")
print(f"Total events: {len(pivot)}")
print(f"Upgrade events: {(pivot['event_type']=='upgrade').sum()}")
print(f"Downgrade events: {(pivot['event_type']=='downgrade').sum()}")

# Group by event type
summary = pivot.groupby('event_type').agg({
    'conv_count': ['mean', 'std', 'count'],
    'before_conv_count': 'mean',
    'after_conv_count': 'mean',
    'conv_delta': 'mean',
    'conv_change_pct': 'mean',
    'bug_delta': 'mean',
    'outage_delta': 'mean',
    'escalation_delta': 'mean',
    'sla_breach_delta': 'mean',
    'before_bug_count': 'mean',
    'after_bug_count': 'mean',
    'before_outage_count': 'mean',
    'after_outage_count': 'mean',
    'before_sla_breach_count': 'mean',
    'after_sla_breach_count': 'mean',
    'before_avg_rating': 'mean',
    'after_avg_rating': 'mean'
})
print("\n=== Summary Statistics ===")
print(summary.round(2))

# Also compute average per-event metrics
print("\n=== Average per-event metrics ===")
for evt_type in ['upgrade', 'downgrade']:
    sub = pivot[pivot['event_type'] == evt_type]
    print(f"\n--- {evt_type.upper()} events ({len(sub)} total) ---")
    print(f"  Avg convs before: {sub['before_conv_count'].mean():.2f}")
    print(f"  Avg convs after:  {sub['after_conv_count'].mean():.2f}")
    print(f"  Avg conv delta:   {sub['conv_delta'].mean():.2f}")
    print(f"  Avg conv change%: {sub['conv_change_pct'].mean():.1f}%")
    print(f"  Avg bug before:   {sub['before_bug_count'].mean():.2f}")
    print(f"  Avg bug after:    {sub['after_bug_count'].mean():.2f}")
    print(f"  Avg outage before: {sub['before_outage_count'].mean():.2f}")
    print(f"  Avg outage after:  {sub['after_outage_count'].mean():.2f}")
    print(f"  Avg SLA breach before: {sub['before_sla_breach_count'].mean():.2f}")
    print(f"  Avg SLA breach after:  {sub['after_sla_breach_count'].mean():.2f}")
    print(f"  Avg rating before: {sub['before_avg_rating'].mean():.2f}")
    print(f"  Avg rating after:  {sub['after_avg_rating'].mean():.2f}")

# Statistical tests (t-test for before vs after within each group)
print("\n=== Statistical Tests (paired t-test: before vs after) ===")
for evt_type in ['upgrade', 'downgrade']:
    sub = pivot[pivot['event_type'] == evt_type]
    print(f"\n--- {evt_type.upper()} ---")
    for metric, label in [('before_conv_count', 'after_conv_count', 'Conversation count'),
                          ('before_bug_count', 'after_bug_count', 'Bug count'),
                          ('before_outage_count', 'after_outage_count', 'Outage count'),
                          ('before_sla_breach_count', 'after_sla_breach_count', 'SLA breaches')]:
        before = sub[metric[0]]
        after = sub[metric[1]]
        if len(before) > 1 and len(after) > 1:
            t_stat, p_val = stats.ttest_rel(after, before)
            print(f"  {label}: before={before.mean():.2f}, after={after.mean():.2f}, t={t_stat:.3f}, p={p_val:.4f}")
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Retrieve comprehensive data from db
df = db.frame(db.query("""
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COALESCE(ROUND(AVG(al."Anomaly Score"),1),0) AS avg_anom_score,
       COALESCE(SUM(al."Device Anomaly Indicators"),0) AS device_ind,
       COALESCE(SUM(al."Network Anomaly Indicators"),0) AS net_ind,
       COALESCE(SUM(al."Behavior Anomaly Indicators"),0) AS beh_ind,
       COUNT(DISTINCT se."Event ID") AS events,
       COALESCE(SUM(se."Risk Score"),0) AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events,
       COUNT(DISTINCT CASE WHEN se."Severity"='Severe' THEN se."Event ID" END) AS severe_events,
       COUNT(DISTINCT sl."Log ID") AS logs,
       COUNT(DISTINCT CASE WHEN sl."Log Level"='ERROR' THEN sl."Log ID" END) AS error_logs
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
LEFT JOIN system_logs_table sl ON sl."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomalies DESC
"""))

print("Aggregated data:")
print(df.to_string())
print()

# Compute composite weakness score
# Normalize each metric to 0-1 scale
metrics = ['failures', 'anomalies', 'avg_anom_score', 'device_ind', 'net_ind', 'beh_ind', 
           'events', 'risk_sum', 'high_events', 'severe_events', 'error_logs']

for m in metrics:
    col = m + '_norm'
    mn, mx = df[m].min(), df[m].max()
    if mx > mn:
        df[col] = (df[m] - mn) / (mx - mn)
    else:
        df[col] = 0

# Weighted composite weakness score
# Anomalies and security events are the most important indicators of weak points
weights = {
    'failures_norm': 0.10,
    'anomalies_norm': 0.20,
    'avg_anom_score_norm': 0.10,
    'device_ind_norm': 0.05,
    'net_ind_norm': 0.05,
    'beh_ind_norm': 0.05,
    'events_norm': 0.15,
    'risk_sum_norm': 0.10,
    'high_events_norm': 0.10,
    'severe_events_norm': 0.05,
    'error_logs_norm': 0.05
}

df['weakness_score'] = sum(df[c] * w for c, w in weights.items())
df['rank'] = df['weakness_score'].rank(ascending=False)

df_sorted = df.sort_values('weakness_score', ascending=False)
print("Ranked by weakness score:")
print(df_sorted[['login_method','tfa_method','logins','failures','anomalies','events','high_events','risk_sum','weakness_score','rank']].to_string())

# Also compute failure rate per combo
df['failure_rate'] = round(df['failures'] / df['logins'] * 100, 1)
print("\n\nFailure rates:")
print(df[['login_method','tfa_method','logins','failures','failure_rate']].to_string())

# ---- Visualization ----

# 1. Heatmap of weakness scores
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Pivot data for heatmap
pivot_weak = df.pivot_table(index='login_method', columns='tfa_method', values='weakness_score', aggfunc='mean')
pivot_anom = df.pivot_table(index='login_method', columns='tfa_method', values='anomalies', aggfunc='mean')

sns.heatmap(pivot_weak, annot=True, fmt='.3f', cmap='YlOrRd', ax=axes[0])
axes[0].set_title('Composite Weakness Score\n(Login Method × 2FA Method)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Two-Factor Authentication Method')
axes[0].set_ylabel('Login Method')

sns.heatmap(pivot_anom, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[1])
axes[1].set_title('Total Anomaly Count\n(Login Method × 2FA Method)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Two-Factor Authentication Method')
axes[1].set_ylabel('Login Method')

plt.tight_layout()
plt.savefig('/work/weakness_heatmap.png', dpi=150)
plt.close()

# 2. Bar chart of weakness scores with breakdown
fig, ax = plt.subplots(figsize=(14, 7))

combos = [f"{r['login_method']}\n+{r['tfa_method']}" for _, r in df_sorted.iterrows()]
x = np.arange(len(combos))
width = 0.2

# Stacked bars
b1 = ax.bar(x - 1.5*width, df_sorted['anomalies_norm'], width, label='Anomalies', color='#e74c3c')
b2 = ax.bar(x - 0.5*width, df_sorted['events_norm'], width, label='Security Events', color='#f39c12')
b3 = ax.bar(x + 0.5*width, df_sorted['failures_norm'], width, label='Failures', color='#3498db')
b4 = ax.bar(x + 1.5*width, df_sorted['risk_sum_norm'], width, label='Risk Score', color='#9b59b6')

ax.set_xticks(x)
ax.set_xticklabels(combos, fontsize=9, rotation=30, ha='right')
ax.set_ylabel('Normalized Score (0-1)', fontsize=12)
ax.set_title('Weak Point Analysis: Normalized Risk Indicators by Login-2FA Combination', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/weakness_breakdown.png', dpi=150)
plt.close()

# 3. Security event severity distribution
fig, ax = plt.subplots(figsize=(14, 6))

df_sev = db.frame(db.query("""
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       se."Severity",
       COUNT(*) AS cnt
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY 1,2,3
"""))

df_sev['combo'] = df_sev['login_method'] + '\n+' + df_sev['tfa_method']
pivot_sev = df_sev.pivot_table(index='combo', columns='Severity', values='cnt', aggfunc='sum', fill_value=0)
sev_order = ['Low', 'Medium', 'High', 'Severe']
pivot_sev = pivot_sev.reindex(columns=[c for c in sev_order if c in pivot_sev.columns], fill_value=0)

pivot_sev.plot(kind='bar', stacked=True, ax=ax, color=['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c'])
ax.set_title('Security Event Severity Distribution by Login-2FA Combination', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Security Events')
ax.set_xlabel('Login Method + 2FA Method')
ax.legend(title='Severity')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig('/work/severity_distribution.png', dpi=150)
plt.close()

# 4. Anomaly indicator pie/radar for top combos
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

top_combos = df_sorted.head(6)
for i, (_, row) in enumerate(top_combos.iterrows()):
    ax = axes[i]
    labels = ['Device\nAnomaly', 'Network\nAnomaly', 'Behavior\nAnomaly']
    sizes = [row['device_ind'], row['net_ind'], row['beh_ind']]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%', 
                                       colors=colors, startangle=90, textprops={'fontsize':9})
    ax.set_title(f"{row['login_method']} + {row['tfa_method']}\n(Weakness: {row['weakness_score']:.3f})", 
                 fontsize=10, fontweight='bold')

plt.suptitle('Anomaly Indicator Composition for Top Weakest Combinations', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/anomaly_composition.png', dpi=150)
plt.close()

print("\n\nFigures saved to /work/")
print("Analysis complete.")
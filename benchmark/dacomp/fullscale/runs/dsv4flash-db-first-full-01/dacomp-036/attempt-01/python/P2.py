import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 2FA status effect data
df2fa = db.frame(db.query("""
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Status" AS tfa_status,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),3) AS anom_per_login,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       ROUND(1.0*SUM(se."Risk Score")/COUNT(DISTINCT lr."Login Record ID"),1) AS risk_per_login
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY 1,2
"""))

methods = df2fa['login_method'].unique()
x = np.arange(len(methods))
width = 0.35

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Anomalies per login
enabled_anom = df2fa[df2fa['tfa_status']=='Enabled'].set_index('login_method')['anom_per_login'].reindex(methods)
noten_anom = df2fa[df2fa['tfa_status']=='Not Enabled'].set_index('login_method')['anom_per_login'].reindex(methods)

axes[0].bar(x - width/2, enabled_anom.values, width, label='2FA Enabled', color='#2ecc71')
axes[0].bar(x + width/2, noten_anom.values, width, label='2FA Not Enabled', color='#e74c3c')
axes[0].set_xticks(x); axes[0].set_xticklabels(methods, rotation=15)
axes[0].set_title('Anomalies per Login by 2FA Status (2024)', fontweight='bold')
axes[0].set_ylabel('Anomalies per Login')
axes[0].legend(); axes[0].grid(axis='y', alpha=0.3)

# Risk per login
enabled_risk = df2fa[df2fa['tfa_status']=='Enabled'].set_index('login_method')['risk_per_login'].reindex(methods)
noten_risk = df2fa[df2fa['tfa_status']=='Not Enabled'].set_index('login_method')['risk_per_login'].reindex(methods)

axes[1].bar(x - width/2, enabled_risk.values, width, label='2FA Enabled', color='#2ecc71')
axes[1].bar(x + width/2, noten_risk.values, width, label='2FA Not Enabled', color='#e74c3c')
axes[1].set_xticks(x); axes[1].set_xticklabels(methods, rotation=15)
axes[1].set_title('Security Risk Score per Login by 2FA Status (2024)', fontweight='bold')
axes[1].set_ylabel('Total Risk Score per Login')
axes[1].legend(); axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/2fa_status_effect.png', dpi=150)
plt.close()

# Summary ranking bar chart (final recommendation)
df_sum = db.frame(db.query("""
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
"""))

# Normalize and compute weakness score same as before
metrics = ['failures','anomalies','avg_anom_score','events','risk_sum','high_events']
for m in metrics:
    mn, mx = df_sum[m].min(), df_sum[m].max()
    df_sum[m+'_n'] = (df_sum[m]-mn)/(mx-mn) if mx>mn else 0
df_sum['weakness'] = (0.15*df_sum['failures_n'] + 0.25*df_sum['anomalies_n'] + 0.10*df_sum['avg_anom_score_n']
                     + 0.20*df_sum['events_n'] + 0.15*df_sum['risk_sum_n'] + 0.15*df_sum['high_events_n'])
df_sum = df_sum.sort_values('weakness', ascending=True)  # ascending: best (lowest weakness) first

fig, ax = plt.subplots(figsize=(12, 7))
combos = [f"{r['login_method']} + {r['tfa_method']}" for _, r in df_sum.iterrows()]
colors = plt.cm.RdYlGn(np.linspace(0.15, 0.85, len(df_sum)))  # green=good, red=bad
bars = ax.barh(combos, df_sum['weakness'].values, color=colors)
ax.set_xlabel('Composite Weakness Score (lower = better)', fontsize=12)
ax.set_title('Login-2FA Combinations Ranked by Weakness (2024)', fontweight='bold', fontsize=14)
for idx, (_, row) in enumerate(df_sum.iterrows()):
    ax.text(row['weakness']+0.008, idx, f"{row['logins']} logins | {row['anomalies']} anom | {row['events']} evt",
            va='center', fontsize=8, color='#444')
plt.tight_layout()
plt.savefig('/work/ranking.png', dpi=150)
plt.close()

print(df_sum[['login_method','tfa_method','logins','failures','anomalies','events','risk_sum','weakness']].to_string())
print("\nFigures saved.")
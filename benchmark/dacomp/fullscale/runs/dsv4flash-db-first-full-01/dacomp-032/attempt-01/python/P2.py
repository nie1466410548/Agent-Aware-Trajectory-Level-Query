import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'figure.dpi': 100, 'font.size': 9})

tk = db.frame(db.query("""
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu,
t."Ticket priority" AS tprio
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
"""))
cp = db.frame(db.query("""
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS speed_h,
cp."Complaint Customer Satisfaction" AS sat, cp."Whether Complaint Was Escalated" AS escalated,
cp."Complaint Type Serial Number" AS ctype
FROM complaints_table cp
JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID"
JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"
"""))

# Fig 1: Ticket metrics boxplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
order = ['Priority 1', 'Other']
sns.boxplot(x='grp', y='res_h', data=tk, order=order, ax=axes[0], palette=['#d62728','#7f8c8d'])
axes[0].set_title('Ticket resolution duration (hours)')
axes[0].set_xlabel('')
sns.boxplot(x='grp', y='sat', data=tk, order=order, ax=axes[1], palette=['#d62728','#7f8c8d'])
axes[1].set_title('Ticket customer satisfaction (1-5)')
axes[1].set_xlabel('')
plt.tight_layout()
plt.savefig('work/fig1_ticket_metrics.png')
plt.close()

# Fig 2: Complaint metrics boxplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.boxplot(x='grp', y='speed_h', data=cp, order=order, ax=axes[0], palette=['#d62728','#7f8c8d'])
axes[0].set_title('Complaint handling speed (hours)')
axes[0].set_xlabel('')
sns.boxplot(x='grp', y='sat', data=cp, order=order, ax=axes[1], palette=['#d62728','#7f8c8d'])
axes[1].set_title('Complaint satisfaction (1-5)')
axes[1].set_xlabel('')
plt.tight_layout()
plt.savefig('work/fig2_complaint_metrics.png')
plt.close()

# Fig 3: Priority-1 ticket urgency distribution + avg metrics
p1 = tk[tk.grp=='Priority 1']
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
urg_agg = p1.groupby('urgency').agg(cnt=('res_h','size'), avg_res=('res_h','mean'), avg_sat=('sat','mean')).reindex(['High','Medium','Low']).fillna(0)
axes[0].bar(urg_agg.index, urg_agg['cnt'], color=['#c0392b','#f39c12','#27ae60'])
axes[0].set_title('Priority-1 tickets by urgency (n)')
axes[0].set_ylabel('Number of tickets')
x = np.arange(3); w=0.35
axes[1].bar(x-w/2, urg_agg['avg_res'], w, label='Avg resolution hours', color='#2980b9')
axes[1].bar(x+w/2, urg_agg['avg_sat'], w, label='Avg satisfaction (x2 for scale)', color='#e74c3c')
axes[1].set_xticks(x); axes[1].set_xticklabels(urg_agg.index)
axes[1].legend(); axes[1].set_title('Priority-1 tickets: urgency vs performance')
plt.tight_layout()
plt.savefig('work/fig3_urgency.png')
plt.close()

# Fig 4: satisfaction distribution comparison (stacked normalized)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sat_tk = pd.crosstab(tk.grp, tk.sat, normalize='index')*100
sat_tk.loc[['Priority 1','Other']].T.plot(kind='bar', ax=axes[0], color=['#d62728','#7f8c8d'])
axes[0].set_title('Ticket satisfaction distribution (%)')
axes[0].set_xlabel('Satisfaction score'); axes[0].legend(title='')
sat_cp = pd.crosstab(cp.grp, cp.sat, normalize='index')*100
sat_cp.loc[['Priority 1','Other']].T.plot(kind='bar', ax=axes[1], color=['#d62728','#7f8c8d'])
axes[1].set_title('Complaint satisfaction distribution (%)')
axes[1].set_xlabel('Satisfaction score'); axes[1].legend(title='')
plt.tight_layout()
plt.savefig('work/fig4_satisfaction_dist.png')
plt.close()

print("Figures saved. Ticket counts:", tk.grp.value_counts().to_dict())
print("Complaint counts:", cp.grp.value_counts().to_dict())
print("P1 tickets by urgency:\n", p1.groupby('urgency').size())
print("P1 satisfaction ticket avg by urgency:\n", p1.groupby('urgency')['sat'].mean().round(2))

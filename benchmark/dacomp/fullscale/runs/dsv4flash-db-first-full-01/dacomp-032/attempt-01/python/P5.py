import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Overlapping work orders with both ticket and complaint data for priority-1
overlap = db.frame(db.query("""
SELECT t."Work Order ID", t."Ticket customer satisfaction score" AS ticket_sat,
t."Ticket resolution duration" AS res_h, cp."Complaint Customer Satisfaction" AS comp_sat,
cp."Complaint Type Serial Number" AS ctype,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS comp_speed
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
JOIN complaints_table cp ON cp."Work Order ID" = t."Work Order ID"
WHERE cc."Contact priority" = 1
"""))

print("=== Overlap (work orders with both ticket and complaint) ===")
print(f"Count: {len(overlap)}")
print(f"Mean ticket sat: {overlap['ticket_sat'].mean():.2f}, Mean comp sat: {overlap['comp_sat'].mean():.2f}")
print(f"Correlation ticket_sat vs comp_sat: {overlap['ticket_sat'].corr(overlap['comp_sat']):.3f}")
print(f"Correlation res_h vs comp_speed: {overlap['res_h'].corr(overlap['comp_speed']):.3f}")

# Spearman correlation (non-parametric)
r,p = stats.spearmanr(overlap['ticket_sat'], overlap['comp_sat'])
print(f"Spearman ticket_sat vs comp_sat: r={r:.3f}, p={p:.4f}")

# By complaint type
print("\n=== By complaint type ===")
ct = overlap.groupby('ctype').agg(n=('Work Order ID','size'), 
                                  avg_ticket_sat=('ticket_sat','mean'),
                                  avg_comp_sat=('comp_sat','mean'),
                                  avg_res_h=('res_h','mean'),
                                  avg_comp_speed=('comp_speed','mean')).round(2)
print(ct)

# Scatter plot: ticket sat vs complaint sat
fig, ax = plt.subplots(figsize=(6,5))
# Add jitter for visibility
jitter = 0.1
x = overlap['ticket_sat'] + np.random.uniform(-jitter,jitter,len(overlap))
y = overlap['comp_sat'] + np.random.uniform(-jitter,jitter,len(overlap))
ax.scatter(x, y, alpha=0.7, s=50, c=overlap['ctype'], cmap='Set1')
ax.set_xlabel('Ticket satisfaction')
ax.set_ylabel('Complaint satisfaction')
ax.set_title('Priority-1: Ticket vs Complaint satisfaction\n(22 overlapping work orders)')
ax.set_xticks([1,2,3,4,5])
ax.set_yticks([1,2,3,4,5])
# Add trend line
m,b = np.polyfit(overlap['ticket_sat'], overlap['comp_sat'], 1)
ax.plot([1,5], [m*1+b, m*5+b], 'k--', alpha=0.5)
plt.tight_layout()
plt.savefig('work/fig5_overlap_scatter.png')
plt.close()

# Heatmap of satisfaction co-occurrence
ct_sat = pd.crosstab(overlap['ticket_sat'], overlap['comp_sat'], margins=True)
print("\n=== Ticket sat x Comp sat cross-tab (priority-1 overlap) ===")
print(ct_sat)

# Coverage analysis for priority-1: proportion that have tickets/complaints
print("\n=== Coverage among priority-1 customers ===")
print(f"Total priority-1 customers: 105")
print(f"With tickets: 27 (25.7%)")
print(f"With complaints: 25 (23.8%)")
print(f"With either: 41 (39.0%)")
print(f"With both: {len(overlap)} (21.0%)")

# Ticket satisfaction by urgency for priority-1
tk = db.frame(db.query("""
SELECT CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
"""))

p1 = tk[tk.grp=='Priority 1']
print("\n=== Priority-1: urgency vs satisfaction ===")
urg_sat = p1.groupby('urgency', observed=False).agg(n=('sat','size'), avg_sat=('sat','mean'), med_sat=('sat','median'))
print(urg_sat)

# Kruskal-Wallis test: satisfaction across urgency levels for priority-1
h_urg = p1[p1.urgency.isin(['High','Medium','Low'])]
groups = [h_urg[h_urg.urgency==u]['sat'] for u in ['High','Medium','Low']]
if all(len(g)>0 for g in groups):
    h,p_val = stats.kruskal(*groups)
    print(f"Kruskal-Wallis (sat by urgency, P1): H={h:.3f}, p={p_val:.4f}")

# Compare avg resolution duration for priority-1 vs other by urgency
print("\n=== Avg resolution by urgency ===")
print(tk.groupby(['grp','urgency'], observed=False).agg(n=('res_h','size'), avg=('res_h','mean')).round(1))
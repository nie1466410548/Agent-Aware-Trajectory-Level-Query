import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Retrieve joined ticket data (already joined in SQL)
tk = db.frame(db.query("""
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu
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

print("=== TICKET DATA ===")
print(tk.groupby('grp').agg(n=('res_h','size'), avg_res_h=('res_h','mean'), med_res_h=('res_h','median'),
                            avg_sat=('sat','mean'), sfu_pct=('sfu', lambda x: 100*(x=='Yes').mean())).round(2))
print("\n=== COMPLAINT DATA ===")
print(cp.groupby('grp').agg(n=('speed_h','size'), avg_speed_h=('speed_h','mean'), med_speed_h=('speed_h','median'),
                            avg_sat=('sat','mean'), esc_pct=('escalated', lambda x: 100*(x=='Yes').mean())).round(2))

# Statistical tests
p1 = tk[tk.grp=='Priority 1']; oth = tk[tk.grp=='Other']
for col, name in [('res_h','Ticket resolution duration (h)'), ('sat','Ticket satisfaction')]:
    u,p = stats.mannwhitneyu(p1[col], oth[col], alternative='two-sided')
    print(f"Mann-Whitney {name}: U={u:.0f}, p={p:.4f}  (P1 median={p1[col].median()}, Other median={oth[col].median()})")

p1c = cp[cp.grp=='Priority 1']; othc = cp[cp.grp=='Other']
for col, name in [('speed_h','Complaint handling speed (h)'), ('sat','Complaint satisfaction')]:
    u,p = stats.mannwhitneyu(p1c[col], othc[col], alternative='two-sided')
    print(f"Mann-Whitney {name}: U={u:.0f}, p={p:.4f}  (P1 median={p1c[col].median()}, Other median={othc[col].median()})")

# Chi-square for second-follow-up rate and escalation rate
from scipy.stats import chi2_contingency
ct_sfu = pd.crosstab(tk.grp, tk.sfu)
chi2,p,_,_ = chi2_contingency(ct_sfu)
print(f"\nChi-square second follow-up (P1 vs Other): chi2={chi2:.2f}, p={p:.4f}")
print(pd.crosstab(tk.grp, tk.sfu, normalize='index').round(3))

ct_esc = pd.crosstab(cp.grp, cp.escalated)
chi2,p,_,_ = chi2_contingency(ct_esc)
print(f"Chi-square complaint escalation (P1 vs Other): chi2={chi2:.2f}, p={p:.4f}")
print(pd.crosstab(cp.grp, cp.escalated, normalize='index').round(3))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Price sensitivity and spending power by age group
r = db.query("""
SELECT u."Age group" as age, 
  t."Price Sensitivity" as ps, 
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"
""")
ps = db.frame(r)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
ages = ["<25","25-35","36-50","50+"]
x = np.arange(len(ages))
w = 0.25

# Price sensitivity
ax = axes[0]
for i, ps_level in enumerate(["High","Medium","Low"]):
    subset = ps[ps["ps"]==ps_level].set_index("age").reindex(ages)
    ax.bar(x + i*w, subset["cnt"], w, label=ps_level, edgecolor='black')
ax.set_xticks(x + w)
ax.set_xticklabels(ages)
ax.set_ylabel("User count")
ax.set_title("Price Sensitivity by Age Group")
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Spending power
r2 = db.query("""
SELECT u."Age group" as age, 
  t."Spending Power" as sp, 
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Spending Power"
""")
sp = db.frame(r2)
ax = axes[1]
for i, sp_level in enumerate(["Weak","Medium","Strong"]):
    subset = sp[sp["sp"]==sp_level].set_index("age").reindex(ages)
    ax.bar(x + i*w, subset["cnt"], w, label=sp_level, edgecolor='black')
ax.set_xticks(x + w)
ax.set_xticklabels(ages)
ax.set_ylabel("User count")
ax.set_title("Spending Power by Age Group")
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("fig7_price_spending.png", dpi=150)
plt.close()
print("fig7 saved")

# High-value & potential conversion by age
r3 = db.query("""
SELECT u."Age group" as age, 
  t."Is High-Value User" as hv,
  t."Is Potential Conversion User" as pc,
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User", t."Is Potential Conversion User"
""")
hpc = db.frame(r3)
hpc_pivot = hpc.groupby(["age","hv","pc"])["cnt"].sum().reset_index()
print("--- High-Value & Potential Conversion ---")
print(hpc_pivot.to_string())

# At-risk rate by hi/lo value
r4 = db.query("""
SELECT u."Age group" as age, 
  t."Is High-Value User" as hv,
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User"
""")
hv_risk = db.frame(r4)
print("\n--- At-risk by high-value status ---")
print(hv_risk.to_string())

# Top 3 campaigns by rating for each age group
r5 = db.query("""
SELECT age, evt, interactions, avg_rating, avg_shares, avg_conv, used_pct
FROM (
  SELECT 
    u."Age group" as age,
    m."Event Name" as evt,
    COUNT(*) as interactions,
    ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
    ROUND(AVG(m."Number of Shares"),1) as avg_shares,
    ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
    ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
    ROW_NUMBER() OVER (PARTITION BY u."Age group" ORDER BY AVG(m."Event Feedback Rating") DESC) as rn
  FROM user_basic_information_table_1 u
  JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
  GROUP BY u."Age group", m."Event Name"
  HAVING COUNT(*) >= 3
)
WHERE rn <= 3
""")
top3 = db.frame(r5)
print("\n--- Top 3 campaigns by rating per age group ---")
print(top3.to_string())
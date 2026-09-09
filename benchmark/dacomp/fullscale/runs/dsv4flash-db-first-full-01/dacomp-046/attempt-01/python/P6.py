import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Pull browsing preferences exact
r1 = db.query("""
SELECT u."Age group" as age, t."Browsing Preference Tag" as pref, COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
WHERE t."Browsing Preference Tag" != 'None'
GROUP BY u."Age group", t."Browsing Preference Tag"
""")
brow = db.frame(r1)
brow.to_csv("browsing_by_age.csv", index=False)

pivot = brow.pivot_table(index="pref", columns="age", values="cnt", aggfunc="sum", fill_value=0)
pivot = pivot[["<25","25-35","36-50","50+"]]
pivot_pct = pivot.div(pivot.sum(axis=0), axis=1)*100

fig, ax = plt.subplots(figsize=(9, 5))
bottom = np.zeros(4)
colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3"]
for idx, (pref, row) in enumerate(pivot_pct.iterrows()):
    vals = row.values
    ax.bar(row.index, vals, bottom=bottom, color=colors[idx], label=pref, edgecolor='black')
    bottom += vals
ax.set_ylabel("Percentage (%)")
ax.set_title("Browsing Preferences by Age Group (non-None tags)")
ax.legend(loc='upper right', fontsize=7)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig("fig4_browsing_preferences.png", dpi=150)
plt.close()
print("fig4 regenerated")
print(pivot.to_string())

# Purchase preferences
r2 = db.query("""
SELECT u."Age group" as age, t."Purchase Preference Tag" as pref, COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
WHERE t."Purchase Preference Tag" != 'None'
GROUP BY u."Age group", t."Purchase Preference Tag"
""")
pur = db.frame(r2)
pur.to_csv("purchase_by_age.csv", index=False)
pp = pur.pivot_table(index="pref", columns="age", values="cnt", aggfunc="sum", fill_value=0)
pp = pp[["<25","25-35","36-50","50+"]]
pp_pct = pp.div(pp.sum(axis=0), axis=1)*100

fig, ax = plt.subplots(figsize=(9, 5))
bottom = np.zeros(4)
colors2 = ["#66c2a5","#fc8d62","#8da0cb","#e78ac3"]
for idx, (pref, row) in enumerate(pp_pct.iterrows()):
    vals = row.values
    ax.bar(row.index, vals, bottom=bottom, color=colors2[idx], label=pref, edgecolor='black')
    bottom += vals
ax.set_ylabel("Percentage (%)")
ax.set_title("Purchase Preferences by Age Group (non-None tags)")
ax.legend(loc='upper right', fontsize=7)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig("fig4b_purchase_preferences.png", dpi=150)
plt.close()
print("fig4b saved")
print(pp.to_string())

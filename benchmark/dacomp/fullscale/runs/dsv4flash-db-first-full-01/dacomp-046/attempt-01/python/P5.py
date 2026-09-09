import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Pull exact data from DB using logged interface
r = db.query("""
SELECT 
  u."Age group" as age,
  m."Event Name" as evt,
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
""")
camp = db.frame(r)
camp.to_csv("campaign_by_age.csv", index=False)
print(camp.shape)
print(camp.head(3))

# Heatmap fig3
pivot = camp.pivot_table(index="evt", columns="age", values="avg_rating", aggfunc="mean")
pivot = pivot[["<25","25-35","36-50","50+"]]
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(pivot.values.astype(float), cmap="RdYlGn", vmin=1, vmax=4.5)
ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index)
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        ax.text(j, i, f"{pivot.values[i][j]:.2f}", ha="center", va="center", color="black", fontsize=8)
ax.set_title("Campaign Feedback Rating by Age Group")
fig.colorbar(im, ax=ax, label="Avg Feedback Rating")
plt.tight_layout()
plt.savefig("fig3_campaign_rating_heatmap.png", dpi=150)
plt.close()
print("fig3 regenerated")

# Figure 3b: top campaigns by interactions per age
top = camp.sort_values("interactions", ascending=False)
top = top.groupby("age").head(3)
print(top[["age","evt","interactions","avg_rating","avg_shares","avg_conv","used_pct"]].to_string())

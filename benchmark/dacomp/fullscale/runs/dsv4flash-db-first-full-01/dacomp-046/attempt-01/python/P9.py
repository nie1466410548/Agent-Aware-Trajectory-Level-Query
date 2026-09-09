import pandas as pd
import numpy as np

# Statistical correlation analysis (not well supported by SQLite)
r = db.query("""
SELECT u."Age group" as age, m."Event Feedback Rating" as rating,
       m."Number of Shares" as shares, m."Event Conversion Rate" as conv,
       m."Event Dwell Time" as dwell, m."Number of Participants" as participants
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
""")
df = db.frame(r)
print("Rows:", len(df))
print(df[["rating","shares","conv","dwell","participants"]].corr().round(3).to_string())

# Per-age correlations
for age in ["<25","25-35","36-50","50+"]:
    sub = df[df["age"]==age]
    if len(sub) > 5:
        c = sub[["rating","shares","conv","dwell"]].corr()
        print(f"\n{age} (n={len(sub)}) corr(rating,shares)={c.loc['rating','shares']:.2f}, corr(rating,conv)={c.loc['rating','conv']:.2f}, corr(shares,conv)={c.loc['shares','conv']:.2f}")

# Share rate per user type
r2 = db.query("""
SELECT u."Age group" as age,
  t."Is At-Risk User" as risk,
  AVG(m."Number of Shares") as avg_shares,
  AVG(m."Event Feedback Rating") as avg_rating,
  AVG(m."Event Conversion Rate") as avg_conv,
  AVG(m."Event Dwell Time") as avg_dwell
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", t."Is At-Risk User"
""")
risk = db.frame(r2)
print("\n--- Campaign behavior by at-risk status ---")
print(risk.to_string())
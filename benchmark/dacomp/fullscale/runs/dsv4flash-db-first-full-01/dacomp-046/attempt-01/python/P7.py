import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Share rate = shares / participants per age group
r = db.query("""
SELECT 
  u."Age group" as age,
  ROUND(100.0*SUM(m."Number of Shares")/NULLIF(SUM(m."Number of Participants"),0),3) as share_rate,
  ROUND(AVG(m."Number of Shares"),2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(100.0*SUM(CASE WHEN m."Is Event Blocked"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as blocked_pct,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
  COUNT(*) as interactions
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
""")
summary = db.frame(r)
print(summary.to_string())

# Gender distribution by age
r2 = db.query("SELECT \"Age group\", \"Gender\", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY \"Age group\", \"Gender\"")
gender_dist = db.frame(r2)
print("\n--- Gender distribution ---")
print(gender_dist.to_string())

# Income level distribution by age
r3 = db.query("SELECT \"Age group\", \"Income level\", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY \"Age group\", \"Income level\"")
inc = db.frame(r3)
print("\n--- Income distribution ---")
print(inc.to_string())

# Education level distribution by age
r4 = db.query("SELECT \"Age group\", \"Education Level\", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY \"Age group\", \"Education Level\"")
edu = db.frame(r4)
print("\n--- Education distribution ---")
print(edu.to_string())
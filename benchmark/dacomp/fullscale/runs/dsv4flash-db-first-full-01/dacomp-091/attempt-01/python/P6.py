import pandas as pd
from collections import defaultdict

# Categorical distribution of selected vendors via db.frame
r2 = db.query("""
  SELECT vendor_tier, payment_risk_level, performance_rating, dependency_level, COUNT(*) AS n
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  GROUP BY vendor_tier, payment_risk_level, performance_rating, dependency_level
  ORDER BY n DESC
""")
dfc = db.frame(r2)
agg = defaultdict(int)
for _, row in dfc.iterrows():
    for k in ['vendor_tier','payment_risk_level','performance_rating','dependency_level']:
        agg[(k, row[k])] += int(row['n'])
print("=== Categorical distribution of selected vendors ===")
for k in ['vendor_tier','payment_risk_level','performance_rating','dependency_level']:
    print(f"\n{k}:")
    for (kk, v), n in sorted(agg.items(), key=lambda x: -x[1]):
        if kk == k:
            print(f"  {v}: {n}")

# Distribution of performance scores and growth
r3 = db.query("""
  SELECT overall_performance_score, COUNT(*) AS n,
         ROUND(AVG(annual_spend_growth_pct),2) AS avg_growth,
         ROUND(MIN(annual_spend_growth_pct),2) AS min_growth,
         ROUND(MAX(annual_spend_growth_pct),2) AS max_growth
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  GROUP BY overall_performance_score ORDER BY overall_performance_score
""")
dfg = db.frame(r3)
print("\n=== Performance score distribution ===")
print(dfg.to_string(index=False))
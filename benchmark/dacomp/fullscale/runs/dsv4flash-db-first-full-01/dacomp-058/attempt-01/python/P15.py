import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Device-level computed ROAS for problematic campaigns
r = db.query("""
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, 
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 3) AS computed_roas,
  ROUND(AVG(roas), 3) AS roas_field,
  ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__device_report
WHERE campaign_id IN ({})
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
dev_computed = db.frame(r)
print("Device-level computed ROAS (cv/cost) for problematic campaigns:")
print(dev_computed.to_string(index=False))

# Geo-level computed ROAS for problematic campaigns
r = db.query("""
SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 3) AS computed_roas,
  ROUND(AVG(roas), 3) AS roas_field,
  ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN ({})
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, geo_target
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
geo_computed = db.frame(r)
print("\nGeo-level computed ROAS (cv/cost) for problematic campaigns:")
print(geo_computed.to_string(index=False))

# Device optimization: find best/worst device per campaign by computed_roas
print("\n\n=== Device Optimization Recommendations ===")
for cid in problematic_ids:
    dev_c = dev_computed[dev_computed['campaign_id']==cid].sort_values('computed_roas', ascending=False)
    if len(dev_c) > 0:
        best = dev_c.iloc[0]
        worst = dev_c.iloc[-1]
        print(f"Campaign {cid} (roas_field={best['roas_field']}):")
        print(f"  Best device: {best['device_type']} (computed ROAS={best['computed_roas']}, cost={best['cost']:,.0f})")
        print(f"  Worst device: {worst['device_type']} (computed ROAS={worst['computed_roas']}, cost={worst['cost']:,.0f})")

# Geo optimization
print("\n\n=== Geo Optimization Recommendations ===")
for cid in problematic_ids:
    geo_c = geo_computed[geo_computed['campaign_id']==cid].sort_values('computed_roas', ascending=False)
    if len(geo_c) > 0:
        best = geo_c.iloc[0]
        worst = geo_c.iloc[-1]
        print(f"Campaign {cid} (roas_field={best['roas_field']}):")
        print(f"  Best geo: {best['geo_target']} (computed ROAS={best['computed_roas']}, cost={best['cost']:,.0f})")
        print(f"  Worst geo: {worst['geo_target']} (computed ROAS={worst['computed_roas']}, cost={worst['cost']:,.0f})")
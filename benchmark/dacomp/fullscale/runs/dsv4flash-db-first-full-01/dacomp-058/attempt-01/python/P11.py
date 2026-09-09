import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Keyword report for problematic campaigns
r = db.query("""
SELECT k.* FROM google_ads__keyword_report k ORDER BY k.campaign_id, k.year_quarter
""", parameters=[])
kw = db.frame(r)
print("Keyword report campaigns:", sorted(kw['campaign_id'].unique()))
print("Problematic campaigns in keyword report:", sorted(set(problematic_ids) & set(kw['campaign_id'].unique())))

# Keyword aggregates for problematic campaigns that have keyword data
kw_problematic = kw[kw['campaign_id'].isin(problematic_ids)]
if len(kw_problematic) > 0:
    print("\nKeyword data for problematic campaigns:")
    kw_agg = kw_problematic.groupby(['campaign_id','keyword_text','match_type']).agg(
        impressions=('impressions','sum'), clicks=('clicks','sum'), cost=('cost','sum'),
        conversions=('conversions','sum'), conversion_value=('conversion_value','sum'),
        qs=('quality_score','mean'), avg_pos=('avg_position','mean')).reset_index()
    print(kw_agg.round(2).to_string(index=False))

# Device breakdown for problematic campaigns
r = db.query("""
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr
FROM google_ads__device_report
WHERE campaign_id IN ({})
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
dev_prob = db.frame(r)
print("\nDevice breakdown for problematic campaigns:")
print(dev_prob.to_string(index=False))
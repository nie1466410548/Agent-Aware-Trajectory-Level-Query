import pandas as pd
import numpy as np
import json

# Load ad group data
cols = ['ad_group_id', 'ad_group_name', 'campaign_name', 'account_name', 'status',
        'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S11.rows.jsonl')], columns=cols)

# Load campaign aggregates
cols_c = ['campaign_id', 'campaign_name', 'account_name', 'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S12.rows.jsonl')], columns=cols_c)
# S12 was capped at 1000 rows preview but archived row_count says 1000? Let me check actual file row count
print("Campaign rows loaded:", len(cam))

# Load keyword report for campaign mapping? We need campaign_id on ad group table
# ad_group_report has campaign_id, so join there. But S11 didn't include campaign_id. Let's add it via another query.
print(ag.columns.tolist())

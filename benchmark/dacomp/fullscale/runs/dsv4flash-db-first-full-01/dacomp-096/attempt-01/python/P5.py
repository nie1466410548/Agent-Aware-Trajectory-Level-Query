import json
import pandas as pd

cols16 = ["flow_id","flow_name","campaign_type","audience_bucket","created_at","updated_at","prev_updated_at",
          "hours_since_prev","or_calc","mu_or","sd_or","or_anomaly","ctor_calc","mu_ctor","sd_ctor",
          "ctor_anomaly","freq_anomaly","any_anomaly"]
rows = []
with open('/results/S16.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
an = pd.DataFrame(rows, columns=cols16)
print("Total campaigns:", len(an))
print("Anomaly counts:")
print(an[['or_anomaly','ctor_anomaly','freq_anomaly','any_anomaly']].sum())

flagged = an[an['any_anomaly']==1]
print("\nFlagged campaigns:", len(flagged))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)
print(flagged[['flow_id','flow_name','campaign_type','created_at','updated_at','prev_updated_at','hours_since_prev',
               'or_calc','mu_or','sd_or','or_anomaly','ctor_calc','mu_ctor','sd_ctor','ctor_anomaly','freq_anomaly']].to_string())
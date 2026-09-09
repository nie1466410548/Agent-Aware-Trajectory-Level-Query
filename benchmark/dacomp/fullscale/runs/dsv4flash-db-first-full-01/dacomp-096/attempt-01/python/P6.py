import json, pandas as pd
cols16 = ["flow_id","flow_name","campaign_type","audience_bucket","created_at","updated_at","prev_updated_at",
          "hours_since_prev","or_calc","mu_or","sd_or","or_anomaly","ctor_calc","mu_ctor","sd_ctor",
          "ctor_anomaly","freq_anomaly","any_anomaly"]
rows = []
with open('/results/S16.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
an = pd.DataFrame(rows, columns=cols16)

# Check how close to the boundaries
an['or_z'] = (an['or_calc'] - an['mu_or']) / an['sd_or']
an['ctor_z'] = (an['ctor_calc'] - an['mu_ctor']) / an['sd_ctor']
print("OR z-score range:", an['or_z'].min(), "to", an['or_z'].max())
print("CTOR z-score range:", an['ctor_z'].min(), "to", an['ctor_z'].max())
print("\nMin hours_since_prev:", an['hours_since_prev'].min())
print("Max hours_since_prev:", an['hours_since_prev'].max())

# Find campaigns with largest deviations
print("\nTop 5 highest OR z-scores:")
print(an.nlargest(5, 'or_z')[['flow_id','flow_name','campaign_type','or_calc','or_z']].to_string())
print("\nTop 5 lowest OR z-scores:")
print(an.nsmallest(5, 'or_z')[['flow_id','flow_name','campaign_type','or_calc','or_z']].to_string())
print("\nTop 5 highest CTOR z-scores:")
print(an.nlargest(5, 'ctor_z')[['flow_id','flow_name','campaign_type','ctor_calc','ctor_z']].to_string())
print("\nTop 5 lowest CTOR z-scores:")
print(an.nsmallest(5, 'ctor_z')[['flow_id','flow_name','campaign_type','ctor_calc','ctor_z']].to_string())

# Check hours_since_prev distribution
print("\n\nHours since prev distribution:")
print(an['hours_since_prev'].describe())
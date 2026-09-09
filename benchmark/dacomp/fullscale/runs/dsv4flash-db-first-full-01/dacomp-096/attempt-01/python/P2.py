import json
import pandas as pd

flows = []
with open('/results/S10.rows.jsonl', 'r') as f:
    for line in f:
        flows.append(json.loads(line))

df = pd.DataFrame(flows)
print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFlow names:", sorted(df['flow_name'].unique()))
print("\nN variation IDs:", df['variation_id'].nunique())
print("\nCount_received_email range:", df['count_received_email'].min(), "-", df['count_received_email'].max())
print(df['count_received_email'].describe())
print("\nDate range (created_at):", df['created_at'].min(), "to", df['created_at'].max())
print("\nDate range (updated_at):", df['updated_at'].min(), "to", df['updated_at'].max())
print("\nStatus values:", df['status'].unique())
print("\nTrigger types:", df['trigger_type'].unique())
print("\nSource relations:", df['source_relation'].unique())
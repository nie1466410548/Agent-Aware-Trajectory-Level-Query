import json
import pandas as pd

cols = ["created_at","flow_id","flow_name","status","updated_at","is_archived","trigger_type",
        "source_relation","variation_id","total_count_unique_people","count_received_email",
        "count_opened_email","count_clicked_email","count_placed_order","count_ordered_product",
        "count_refunded_order","gmv_gross","gmv_net","email_open_rate","email_click_to_open_rate",
        "flow_variation_key","active_days","total_placed_orders","total_amount_positive",
        "total_amount_negative","product_view_to_order_rate_flow","gmv_net_flow"]

rows = []
with open('/results/S10.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=cols)
print("Shape:", df.shape)
print("\nFlow names:", sorted(df['flow_name'].unique()))
print("\nN variation IDs:", df['variation_id'].nunique())
print("\ncount_received_email describe:")
print(df['count_received_email'].describe())
print("\nDate range (created_at):", df['created_at'].min(), "to", df['created_at'].max())
print("\nDate range (updated_at):", df['updated_at'].min(), "to", df['updated_at'].max())
print("\nStatus:", df['status'].value_counts().to_dict())
print("\nTrigger types:", df['trigger_type'].value_counts().to_dict())
print("\nSource relations:", df['source_relation'].value_counts().to_dict())
print("\nemail_open_rate describe:\n", df['email_open_rate'].describe())
print("\nemail_click_to_open_rate describe:\n", df['email_click_to_open_rate'].describe())
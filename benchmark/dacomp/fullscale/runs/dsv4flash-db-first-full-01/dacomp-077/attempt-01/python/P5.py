import pandas as pd
import numpy as np
import json

# Load feature + adoption data
feat = pd.read_csv('/work/feature_clv_analysis.csv')

# Get adoption data from DB
adopt = db.frame(db.query("""
SELECT f.feature_id, f.count_visitors, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user
FROM pendo__feature f
JOIN pendo__product_adoption_analytics a ON a.feature_id = f.feature_id
"""))

merged = feat.merge(adopt, on='feature_id', suffixes=('', '_adopt'))
print("Correlation between count_visitors and regular_users:", merged['count_visitors'].corr(merged['regular_users']))
print("Count_visitors stats:", merged['count_visitors'].describe())
print("Regular_users stats:", merged['regular_users'].describe())

# Check how many features have regular_users < 200
print("\nFeatures with regular_users < 200:", (merged['regular_users'] < 200).sum())
print("Features with count_visitors < 200:", (merged['count_visitors'] < 200).sum())

# Check overlap
both_low = merged[(merged['count_visitors'] < 200) & (merged['regular_users'] < 200)]
print("Both low:", len(both_low))
print(both_low[['feature_id','feature_name','count_visitors','regular_users']].to_string())

# Features with regular_users < 200 but count_visitors >= 200
reg_low_only = merged[(merged['regular_users'] < 200) & (merged['count_visitors'] >= 200)]
print("\nregular_users < 200 but count_visitors >= 200:", len(reg_low_only))
print(reg_low_only[['feature_id','feature_name','count_visitors','regular_users']].to_string())

# Features with count_visitors < 200 but regular_users >= 200
cnt_low_only = merged[(merged['count_visitors'] < 200) & (merged['regular_users'] >= 200)]
print("\ncount_visitors < 200 but regular_users >= 200:", len(cnt_low_only))
print(cnt_low_only[['feature_id','feature_name','count_visitors','regular_users']].to_string())
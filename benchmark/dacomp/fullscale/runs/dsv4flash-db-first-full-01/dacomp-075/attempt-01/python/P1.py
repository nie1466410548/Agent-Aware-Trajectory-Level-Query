import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Retrieve focus group data
result = db.query("""
SELECT * FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend DESC
""")
df = db.frame(result)

print(f"Focus group vendors: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(df[['vendor_id','vendor_name','total_vendor_spend','spend_concentration_ratio','strategic_importance_level']].head(10))

# Save full data for later use
df.to_csv('/work/focus_group_vendors.csv', index=False)
print("Saved focus group data")
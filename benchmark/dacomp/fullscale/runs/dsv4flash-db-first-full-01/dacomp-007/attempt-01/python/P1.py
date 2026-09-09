import pandas as pd
import numpy as np
import json

# Read the full data
rows = []
with open('/results/S3.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
print("Department totals:", rows)

# Get full dataset for analysis
result = db.query("SELECT * FROM sheet1")
df = db.frame(result)

print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Attrition distribution: {df['Attrition'].value_counts().to_dict()}")
print(f"Department distribution: {df['Department'].value_counts().to_dict()}")
print(f"\nAttrition by department:")
print(df.groupby('Department')['Attrition'].apply(lambda x: (x=='Yes').sum()/len(x)*100))
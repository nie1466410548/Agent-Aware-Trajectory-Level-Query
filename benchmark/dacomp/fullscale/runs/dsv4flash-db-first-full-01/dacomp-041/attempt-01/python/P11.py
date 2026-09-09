import pandas as pd
merged = pd.read_csv('/work/merged_high.csv')
print("Merged columns:")
for c in merged.columns:
    print(c)
print()
# Check treatment priority columns
tp_cols = [c for c in merged.columns if 'Treatment' in c or 'Priority' in c]
print("Treatment related columns:", tp_cols)
if tp_cols:
    print(merged[tp_cols].head(10))
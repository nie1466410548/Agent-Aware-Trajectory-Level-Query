import pandas as pd
merged = pd.read_csv('/work/merged_high.csv')
print("Treatment Priority raw values:")
for v in merged['Treatment Priority'].unique():
    print(f"  [{v}] -> len={len(v)}")
print()
# The issue is that the CSV was saved with the original values and stripping didn't persist
# Let me strip at read time and check
merged['Treatment Priority'] = merged['Treatment Priority'].str.strip()
print("After strip:")
print(merged['Treatment Priority'].value_counts())
print()
# Now check the crosstab
merged['Risk Assessment Level'] = merged['Risk Assessment Level'].str.strip() if 'Risk Assessment Level' in merged.columns else None
# Actually the risk level came from a different source. Let me just check the original data
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_art['Treatment Priority'] = high_art['Treatment Priority'].str.strip()
print("High art Treatment Priority:")
print(high_art['Treatment Priority'].value_counts())
print("Urgent count:", (high_art['Treatment Priority'] == 'Urgent').sum())
print("High count:", (high_art['Treatment Priority'] == 'High').sum())
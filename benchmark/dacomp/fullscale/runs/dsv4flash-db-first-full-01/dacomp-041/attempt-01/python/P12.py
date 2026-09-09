import pandas as pd
merged = pd.read_csv('/work/merged_high.csv')
print("Treatment Priority values:")
print(merged['Treatment Priority'].value_counts())
print()
print("Material Type values:")
print(merged['Material Type'].value_counts())
print()
# Cross-tab
print(pd.crosstab(merged['Material Type'], merged['Treatment Priority']))
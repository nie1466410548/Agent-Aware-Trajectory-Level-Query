import pandas as pd
high_art = pd.read_csv('/work/high_traffic_artifacts_clean.csv')
high_case = pd.read_csv('/work/high_traffic_cases_clean.csv')

# Check actual values
print("Treatment Priority unique:", [repr(v) for v in high_art['Treatment Priority'].unique()])
print("Environmental Sensitivity unique:", [repr(v) for v in high_art['Environmental Sensitivity'].unique()])
print("Vibration Sensitivity unique:", [repr(v) for v in high_art['Vibration Sensitivity'].unique()])
print("Silica gel unique:", [repr(v) for v in high_case['Silica gel status'].unique()])
print("Maintenance Status unique:", [repr(v) for v in high_case['Maintenance Status'].unique()])

# Let me try a different approach - check if stripping works at read time
high_art2 = pd.read_csv('/work/high_traffic_artifacts.csv')
print("\nOriginal values:")
print("Treatment Priority unique:", [repr(v) for v in high_art2['Treatment Priority'].unique()])

# Explicitly strip
high_art2['Treatment Priority'] = high_art2['Treatment Priority'].str.strip()
print("After strip:", [repr(v) for v in high_art2['Treatment Priority'].unique()])

# Try with apply
high_art2['Environmental Sensitivity'] = high_art2['Environmental Sensitivity'].apply(lambda x: x.strip() if isinstance(x, str) else x)
print("Env Sensitivity after apply:", [repr(v) for v in high_art2['Environmental Sensitivity'].unique()])
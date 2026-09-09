import pandas as pd
import numpy as np

# Final comprehensive data load with proper stripping
NB = '\xa0'
high = pd.read_csv('/work/high_traffic_env.csv')
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')
df_risk = pd.read_csv('/work/high_traffic_risk.csv')
df_all = pd.read_csv('/work/all_env.csv')

# Strip all string columns
for df in [high_art, high_case, df_risk]:
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()

# Build merged with stripped Treatment Priority
merged = high.copy()
merged['hall_id'] = merged['hall_id'].str.strip()
high_art['hall_id'] = high_art['hall_id'].str.strip()
high_case['hall_id'] = high_case['hall_id'].str.strip()
df_risk['Related Gallery References'] = df_risk['Related Gallery References'].str.strip()

merged = merged.merge(high_art, on='hall_id', how='left', suffixes=('_env', '_art'))
merged = merged.merge(high_case, on='hall_id', how='left')
merged = merged.merge(df_risk, left_on='hall_id', right_on='Related Gallery References', how='left')

# Verify
print("Treatment Priority:", merged['Treatment Priority'].value_counts().to_dict())
print("Urgent count:", (merged['Treatment Priority'] == 'Urgent').sum())
print("High count:", (merged['Treatment Priority'] == 'High').sum())

# High risk relics
top_risk = merged[(merged['Treatment Priority'].isin(['Urgent', 'High'])) & (merged['Deterioration Rate'] == 'Rapid')]
print(f"\nTop risk relics (Urgent/High priority + Rapid deterioration): {len(top_risk)}")
cols = ['Cultural Relic Name', 'Material Type', 'Dynasty', 'Preservation Status', 'Deterioration Rate',
        'Condition Assessment Rating', 'Treatment Priority', 'Risk Assessment Level']
if len(top_risk) > 0:
    print(top_risk[cols].head(30).to_string())

# Check condition assessment by risk level
print("\n\nCondition Assessment by Risk Level:")
print(merged.groupby('Risk Assessment Level')['Condition Assessment Rating'].mean())

# Cross-tab
print("\nTreatment Priority by Risk Level:")
print(pd.crosstab(merged['Risk Assessment Level'], merged['Treatment Priority']))

# Preservation Status by Risk Level
print("\nPreservation Status by Risk Level:")
print(pd.crosstab(merged['Risk Assessment Level'], merged['Preservation Status']))

# Material types in high-risk halls
print("\nMaterial Types by Risk Level:")
print(pd.crosstab(merged['Risk Assessment Level'], merged['Material Type']))

# Environmental parameters by risk level
print("\nEnvironmental parameters by Risk Level:")
for col in ['Carbon dioxide concentration (ppm)', 'PM2.5 concentration', NB+'Noise Level (dB)',
            NB+'Vibration Level (mm/s²)', NB+'Microbial Count (CFU)', 'Dust Accumulation (mg/m²)',
            'UV Irradiance (μW/cm²)', NB+'Illuminance (Lux)', 'Temperature (°C)', 'Relative Humidity (%)']:
    print(f"  {col}:")
    for level in ['High', 'Medium', 'Low']:
        subset = merged[merged['Risk Assessment Level'] == level]
        if len(subset) > 0:
            print(f"    {level}: mean={subset[col].mean():.2f}, std={subset[col].std():.2f}")

# Save the clean merged data
merged.to_csv('/work/final_merged_clean.csv', index=False)
print("\nFinal clean merged data saved.")
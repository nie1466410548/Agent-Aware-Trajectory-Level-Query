import pandas as pd
import numpy as np

merged = pd.read_csv('/work/merged_high.csv')
# Strip
for col in merged.columns:
    if merged[col].dtype == 'object':
        merged[col] = merged[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

# Recompute high-risk combos
urgent = merged[merged['Treatment Priority'].isin(['Urgent', 'High'])]
print(f"Urgent/High priority relics: {len(urgent)}")
print(f"  With poor condition (<40): {(urgent['Condition Assessment Rating'] < 40).sum()}")
print(f"  With critical preservation: {(urgent['Preservation Status'] == 'Critical').sum()}")

# Top risk relics
top_risk = merged[(merged['Treatment Priority'] == 'Urgent') & (merged['Condition Assessment Rating'] < 40)]
print(f"\nUrgent priority + condition < 40: {len(top_risk)}")

top_risk2 = merged[(merged['Treatment Priority'].isin(['Urgent','High'])) & (merged['Deterioration Rate'] == 'Rapid')]
print(f"Urgent/High priority + rapid deterioration: {len(top_risk2)}")

# Show some specific examples
print("\nExamples of top risk relics (Urgent + Rapid deterioration):")
cols = ['Cultural Relic Name', 'Material Type', 'Dynasty', 'Preservation Status', 'Deterioration Rate',
        'Condition Assessment Rating', 'Treatment Priority', 'Environmental Sensitivity',
        'Vibration Sensitivity', 'Light Sensitivity', 'Humidity Sensitivity']
if len(top_risk2) > 0:
    print(top_risk2[cols].head(25).to_string())

# Check the risk assessment high-level
df_risk = pd.read_csv('/work/high_traffic_risk.csv')
# map risk to halls and correlate with condition
risk_by_hall = df_risk[['Related Gallery References', 'Risk Assessment Level', 'Conservation Priority Score']]
risk_by_hall['Related Gallery References'] = risk_by_hall['Related Gallery References'].str.strip()
merged2 = merged.merge(risk_by_hall, left_on='hall_id', right_on='Related Gallery References', how='left')
print("\n\n=== RISK LEVEL BY CONDITION RATING ===")
print(merged2.groupby('Risk Assessment Level')['Condition Assessment Rating'].agg(['mean','count']).to_string())
print("\n=== RISK LEVEL BY TREATMENT PRIORITY ===")
ct = pd.crosstab(merged2['Risk Assessment Level'], merged2['Treatment Priority'])
print(ct.to_string())

# Average environmental exposures by risk level
print("\n=== ENV EXPOSURE BY RISK LEVEL ===")
grp = merged2.groupby('Risk Assessment Level')[['Carbon dioxide concentration (ppm)', 
    'PM2.5 concentration', 'Total volatile organic compounds concentration (ppb)', 
    '\xa0Noise Level (dB)', '\xa0Vibration Level (mm/s²)', '\xa0Microbial Count (CFU)']].mean()
print(grp.round(1).to_string())

# Verify: are high-risk halls actually worse environmentally?
print("\n\n=== ENV PARAMS BY FORMAL RISK LEVEL ===")
for col in ['Carbon dioxide concentration (ppm)', 'PM2.5 concentration', '\xa0Noise Level (dB)',
            '\xa0Vibration Level (mm/s²)', '\xa0Microbial Count (CFU)', 'Dust Accumulation (mg/m²)',
            '\xa0Illuminance (Lux)', 'UV Irradiance (μW/cm²)']:
    means = merged2.groupby('Risk Assessment Level')[col].mean()
    print(f"{col}: " + ", ".join([f"{lv}={means.get(lv, float('nan')):.1f}" for lv in ['High', 'Medium', 'Low']]))
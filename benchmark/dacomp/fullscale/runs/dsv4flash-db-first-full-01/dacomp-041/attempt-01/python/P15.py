import pandas as pd
import numpy as np

NB = '\xa0'
high = pd.read_csv('/work/high_traffic_env.csv')
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')
merged = pd.read_csv('/work/merged_high.csv')
df_risk = pd.read_csv('/work/high_traffic_risk.csv')

print("========== KEY FINDINGS SUMMARY ==========")
print(f"Total high-traffic halls (avg >900 visitors/day): {len(high)}")

print("\n--- Environmental Risk Indicators ---")
print(f"1. CO2 > 800 ppm: {(high['Carbon dioxide concentration (ppm)'] > 800).sum()}/{len(high)} ({(high['Carbon dioxide concentration (ppm)'] > 800).mean()*100:.1f}%)")
print(f"2. Noise > 50 dB: {(high[NB+'Noise Level (dB)'] > 50).sum()}/{len(high)} ({(high[NB+'Noise Level (dB)'] > 50).mean()*100:.1f}%)")
print(f"3. TVOC > 300 ppb: {(high['Total volatile organic compounds concentration (ppb)'] > 300).sum()}/{len(high)} ({(high['Total volatile organic compounds concentration (ppb)'] > 300).mean()*100:.1f}%)")
print(f"4. PM2.5 > 25 ug/m3: {(high['PM2.5 concentration'] > 25).sum()}/{len(high)} ({(high['PM2.5 concentration'] > 25).mean()*100:.1f}%)")
print(f"5. Microbial > 400 CFU: {(high[NB+'Microbial Count (CFU)'] > 400).sum()}/{len(high)} ({(high[NB+'Microbial Count (CFU)'] > 400).mean()*100:.1f}%)")
print(f"6. Mold Risk > 0.7: {(high[NB+'Mold Risk Index'] > 0.7).sum()}/{len(high)} ({(high[NB+'Mold Risk Index'] > 0.7).mean()*100:.1f}%)")
print(f"7. Dust > 4 mg/m2: {(high['Dust Accumulation (mg/m²)'] > 4).sum()}/{len(high)} ({(high['Dust Accumulation (mg/m²)'] > 4).mean()*100:.1f}%)")
print(f"8. Vibration > 0.3 mm/s2: {(high[NB+'Vibration Level (mm/s²)'] > 0.3).sum()}/{len(high)} ({(high[NB+'Vibration Level (mm/s²)'] > 0.3).mean()*100:.1f}%)")
print(f"9. 24h Temp change > 1.5C: {(high['24-hour Temperature Change'] > 1.5).sum()}/{len(high)} ({(high['24-hour Temperature Change'] > 1.5).mean()*100:.1f}%)")
print(f"10. 24h RH change > 3%: {(high['24-hour Humidity Change'] > 3).sum()}/{len(high)} ({(high['24-hour Humidity Change'] > 3).mean()*100:.1f}%)")

print("\n--- Artifact Risk Indicators ---")
print(f"1. Rapid deterioration rate: {(high_art['Deterioration Rate'] == 'Rapid').sum()}/{len(high_art)} ({(high_art['Deterioration Rate'] == 'Rapid').mean()*100:.1f}%)")
print(f"2. Urgent treatment priority: {(high_art['Treatment Priority'] == 'Urgent').sum()}/{len(high_art)} ({(high_art['Treatment Priority'] == 'Urgent').mean()*100:.1f}%)")
print(f"3. Critical preservation status: {(high_art['Preservation Status'] == 'Critical').sum()}/{len(high_art)} ({(high_art['Preservation Status'] == 'Critical').mean()*100:.1f}%)")
print(f"4. High environmental sensitivity: {(high_art['Environmental Sensitivity'] == 'High').sum()}/{len(high_art)} ({(high_art['Environmental Sensitivity'] == 'High').mean()*100:.1f}%)")
print(f"5. Poor condition (rating < 25): {(merged['Condition Assessment Rating'] < 25).sum()}/{len(merged)} ({(merged['Condition Assessment Rating'] < 25).mean()*100:.1f}%)")
print(f"6. High vibration sensitivity: {(high_art['Vibration Sensitivity'] == 'High').sum()}/{len(high_art)} ({(high_art['Vibration Sensitivity'] == 'High').mean()*100:.1f}%)")
print(f"7. High light sensitivity: {(high_art['Light Sensitivity'] == 'High').sum()}/{len(high_art)} ({(high_art['Light Sensitivity'] == 'High').mean()*100:.1f}%)")

print("\n--- Display Case Risk Indicators ---")
print(f"1. Poor seal status: {(high_case['Seal status'] == 'Poor').sum()}/{len(high_case)} ({(high_case['Seal status'] == 'Poor').mean()*100:.1f}%)")
print(f"2. Filter Replace Now: {(high_case['Filter status'] == 'Replace Now').sum()}/{len(high_case)} ({(high_case['Filter status'] == 'Replace Now').mean()*100:.1f}%)")
print(f"3. Silica gel Replace Now: {(high_case['Silica gel status'] == 'Replace Now').sum()}/{len(high_case)} ({(high_case['Silica gel status'] == 'Replace Now').mean()*100:.1f}%)")
print(f"4. Maintenance Overdue: {(high_case['Maintenance Status'] == 'Overdue').sum()}/{len(high_case)} ({(high_case['Maintenance Status'] == 'Overdue').mean()*100:.1f}%)")

print("\n--- Risk Assessment ---")
print(df_risk['Risk Assessment Level'].value_counts().to_string())
print(f"Mean Conservation Priority Score: {df_risk['Conservation Priority Score'].mean():.1f}")

# Which relics are in highest risk: combine condition + material + treatment priority
print("\n\n--- TOP RISK RELICS (Condition < 40 AND urgent/high priority) ---")
high_risk = merged[(merged['Condition Assessment Rating'] < 40) & (merged['Treatment Priority'].isin(['Urgent', 'High']))]
print(f"Count: {len(high_risk)}")
cols = ['Cultural Relic Name', 'Material Type', 'Dynasty', 'Preservation Status', 'Deterioration Rate',
        'Condition Assessment Rating', 'Treatment Priority', 'Environmental Sensitivity', 'Vibration Sensitivity', 'Light Sensitivity']
print(high_risk[cols].to_string())

high_risk.to_csv('/work/high_risk_relics.csv', index=False)
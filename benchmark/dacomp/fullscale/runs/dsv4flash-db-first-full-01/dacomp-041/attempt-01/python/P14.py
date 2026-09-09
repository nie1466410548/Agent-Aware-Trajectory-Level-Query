import pandas as pd
import numpy as np

# Query risk assessment data for high-traffic halls
sql = """
SELECT ra.* FROM risk_assessment ra
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(ra."Related Gallery References")
WHERE gi."Daily Visitor Count" > 900
"""
r = db.query(sql)
print(f"Risk assessment rows: {r['executions'][0]['row_count']}")
df_risk = db.frame(r)
print(df_risk.shape)
print(df_risk.head())
df_risk.to_csv('/work/high_traffic_risk.csv', index=False)

# Check risk levels
print("\nRisk Assessment Level distribution:")
print(df_risk['Risk Assessment Level'].value_counts())
print("\nEvacuation Priority:")
print(df_risk['Evacuation Priority'].value_counts())
print("\nConservation Priority Score:")
print(df_risk['Conservation Priority Score'].describe())

# Check usage records
sql2 = """
SELECT ur.* FROM usage_records ur
JOIN artifact_conservation_and_maint acm ON TRIM(acm."Preserve Cultural Relic Reference") = TRIM(ur."Cultural Relic Reference Number")
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
WHERE gi."Daily Visitor Count" > 900
"""
r2 = db.query(sql2)
print(f"\nUsage records: {r2['executions'][0]['row_count']}")
df_usage = db.frame(r2)
print(df_usage.shape)
print("Monitor frequency:")
print(df_usage['monitorfreq'].value_counts())
print("Maint frequency:")
print(df_usage['maintfreq'].value_counts())
print("Assess frequency:")
print(df_usage['assessfreq'].value_counts())
print("Inspect frequency:")
print(df_usage['inspectfreq'].value_counts())

# Final comprehensive analysis summary
print("\n\n========== KEY FINDINGS SUMMARY ==========")
print(f"Total high-traffic halls (avg >900 visitors/day): 104")
print(f"Total low-traffic halls: 846")

# Compute the key risk indicators
print("\n--- Environmental Risk Indicators ---")
print(f"1. CO2 above 800 ppm: {len(high[high['Carbon dioxide concentration (ppm)'] > 800])}/{len(high)} ({len(high[high['Carbon dioxide concentration (ppm)'] > 800])/len(high)*100:.1f}%)")
print(f"2. Noise > 50 dB: {len(high[high[NB+'Noise Level (dB)'] > 50])}/{len(high)} ({len(high[high[NB+'Noise Level (dB)'] > 50])/len(high)*100:.1f}%)")
print(f"3. TVOC > 300 ppb: {len(high[high['Total volatile organic compounds concentration (ppb)'] > 300])}/{len(high)} ({len(high[high['Total volatile organic compounds concentration (ppb)'] > 300])/len(high)*100:.1f}%)")
print(f"4. PM2.5 > 25 ug/m3: {len(high[high['PM2.5 concentration'] > 25])}/{len(high)} ({len(high[high['PM2.5 concentration'] > 25])/len(high)*100:.1f}%)")
print(f"5. Microbial > 400 CFU: {len(high[high[NB+'Microbial Count (CFU)'] > 400])}/{len(high)} ({len(high[high[NB+'Microbial Count (CFU)'] > 400])/len(high)*100:.1f}%)")
print(f"6. Mold Risk > 0.7: {len(high[high[NB+'Mold Risk Index'] > 0.7])}/{len(high)} ({len(high[high[NB+'Mold Risk Index'] > 0.7])/len(high)*100:.1f}%)")
print(f"7. Dust > 4 mg/m2: {len(high[high['Dust Accumulation (mg/m²)'] > 4])}/{len(high)} ({len(high[high['Dust Accumulation (mg/m²)'] > 4])/len(high)*100:.1f}%)")

print("\n--- Artifact Risk Indicators ---")
print(f"1. Rapid deterioration rate: {len(high_art[high_art['Deterioration Rate'] == 'Rapid'])}/{len(high_art)} ({len(high_art[high_art['Deterioration Rate'] == 'Rapid'])/len(high_art)*100:.1f}%)")
print(f"2. Urgent treatment priority: {len(high_art[high_art['Treatment Priority'] == 'Urgent'])}/{len(high_art)} ({len(high_art[high_art['Treatment Priority'] == 'Urgent'])/len(high_art)*100:.1f}%)")
print(f"3. Critical preservation status: {len(high_art[high_art['Preservation Status'] == 'Critical'])}/{len(high_art)} ({len(high_art[high_art['Preservation Status'] == 'Critical'])/len(high_art)*100:.1f}%)")
print(f"4. High environmental sensitivity: {len(high_art[high_art['Environmental Sensitivity'] == 'High'])}/{len(high_art)} ({len(high_art[high_art['Environmental Sensitivity'] == 'High'])/len(high_art)*100:.1f}%)")
print(f"5. Poor condition (rating < 25): {len(merged[merged['Condition Assessment Rating'] < 25])}/{len(merged)} ({len(merged[merged['Condition Assessment Rating'] < 25])/len(merged)*100:.1f}%)")

print("\n--- Display Case Risk Indicators ---")
print(f"1. Poor seal status: {len(high_case[high_case['Seal status'] == 'Poor'])}/{len(high_case)} ({len(high_case[high_case['Seal status'] == 'Poor'])/len(high_case)*100:.1f}%)")
print(f"2. Filter needs replacement: {len(high_case[high_case['Filter status'] == 'Replace Now'])}/{len(high_case)} ({len(high_case[high_case['Filter status'] == 'Replace Now'])/len(high_case)*100:.1f}%)")
print(f"3. Silica gel needs replacement: {len(high_case[high_case['Silica gel status'] == 'Replace Now'])}/{len(high_case)} ({len(high_case[high_case['Silica gel status'] == 'Replace Now'])/len(high_case)*100:.1f}%)")
print(f"4. Maintenance overdue: {len(high_case[high_case['Maintenance Status'] == 'Overdue'])}/{len(high_case)} ({len(high_case[high_case['Maintenance Status'] == 'Overdue'])/len(high_case)*100:.1f}%)")

# Risk assessment level
print(f"\n5. Risk Assessment Level: High={len(df_risk[df_risk['Risk Assessment Level']=='High'])}/104, Critical={len(df_risk[df_risk['Risk Assessment Level']=='Critical'])}/104")
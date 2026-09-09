import pandas as pd
import numpy as np

# Load data
high = pd.read_csv('/work/high_traffic_env.csv')
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')

# Merge environmental with artifact data
merged = high.merge(high_art, on='hall_id', how='left')
merged = merged.merge(high_case, on='hall_id', how='left')
print("Merged shape:", merged.shape)

# Check condition assessment rating distribution
print("\n=== CONDITION ASSESSMENT RATING DISTRIBUTION (High Traffic) ===")
print(merged['Condition Assessment Rating'].describe())
print("\nCounts by bucket:")
bins = [0, 25, 40, 55, 70, 85, 101]
labels = ['0-25 (Critical)', '26-40', '41-55', '56-70', '71-85', '86-100 (Good)']
merged['CondBucket'] = pd.cut(merged['Condition Assessment Rating'], bins=bins, labels=labels)
print(merged['CondBucket'].value_counts().sort_index())

# Correlations between daily visitors and environmental factors
print("\n=== CORRELATION: Daily Visitor Count vs Environmental Parameters (all halls) ===")
df_all = pd.read_csv('/work/all_env.csv')
corr_cols = ['Carbon dioxide concentration (ppm)', 'Total volatile organic compounds concentration (ppb)',
             'PM2.5 concentration', '\xa0Noise Level (dB)', '\xa0Microbial Count (CFU)', 
             'UV Irradiance (μW/cm²)', '\xa0IR Irradiance (W/m²)', 'Dust Accumulation (mg/m²)',
             '\xa0Vibration Level (mm/s²)', 'Temperature (°C)', 'Relative Humidity (%)']
for c in corr_cols:
    if c in df_all.columns:
        corr = df_all['Daily Visitor Count'].corr(df_all[c])
        print(f"{c}: r={corr:.3f}")

# Check which environmental parameters exceed recommended thresholds in high-traffic halls
print("\n=== THRESHOLD EXCEEDANCES (High Traffic Halls) ===")
# CO2 > 800 ppm
co2_high = (high['Carbon dioxide concentration (ppm)'] > 800).sum()
print(f"CO2 > 800 ppm: {co2_high}/{len(high)} ({co2_high/len(high)*100:.1f}%)")
# UV > 75 μW/cm²
uv_high = (high['UV Irradiance (μW/cm²)'] > 75).sum()
print(f"UV > 75 μW/cm²: {uv_high}/{len(high)} ({uv_high/len(high)*100:.1f}%)")
# Illuminance > 200 lux
lux_high = (high['\xa0Illuminance (Lux)'] > 200).sum()
print(f"Illuminance > 200 lux: {lux_high}/{len(high)}")
# Noise > 50 dB
noise_high = (high['\xa0Noise Level (dB)'] > 50).sum()
print(f"Noise > 50 dB: {noise_high}/{len(high)} ({noise_high/len(high)*100:.1f}%)")
# Vibration > 0.3
vib_high = (high['\xa0Vibration Level (mm/s²)'] > 0.3).sum()
print(f"Vibration > 0.3 mm/s²: {vib_high}/{len(high)} ({vib_high/len(high)*100:.1f}%)")
# PM2.5 > 25 (WHO 24h)
pm_high = (high['PM2.5 concentration'] > 25).sum()
print(f"PM2.5 > 25 µg/m³: {pm_high}/{len(high)} ({pm_high/len(high)*100:.1f}%)")
# TVOC > 300 ppb
tvoc_high = (high['Total volatile organic compounds concentration (ppb)'] > 300).sum()
print(f"TVOC > 300 ppb: {tvoc_high}/{len(high)} ({tvoc_high/len(high)*100:.1f}%)")
# Temp change > 1.5°C
tc_high = (high['24-hour Temperature Change'] > 1.5).sum()
print(f"24h Temp change > 1.5°C: {tc_high}/{len(high)} ({tc_high/len(high)*100:.1f}%)")
# RH change > 3%
rc_high = (high['24-hour Humidity Change'] > 3).sum()
print(f"24h RH change > 3%: {rc_high}/{len(high)} ({rc_high/len(high)*100:.1f}%)")
# Mold risk > 0.7
mold_high = (high['\xa0Mold Risk Index'] > 0.7).sum()
print(f"Mold Risk Index > 0.7: {mold_high}/{len(high)} ({mold_high/len(high)*100:.1f}%)")
# Microbial > 400 CFU
mic_high = (high['\xa0Microbial Count (CFU)'] > 400).sum()
print(f"Microbial Count > 400 CFU: {mic_high}/{len(high)} ({mic_high/len(high)*100:.1f}%)")
# Dust > 4 mg/m²
dust_high = (high['Dust Accumulation (mg/m²)'] > 4).sum()
print(f"Dust > 4 mg/m²: {dust_high}/{len(high)} ({dust_high/len(high)*100:.1f}%)")

merged.to_csv('/work/merged_high.csv', index=False)
print("\nMerged saved.")
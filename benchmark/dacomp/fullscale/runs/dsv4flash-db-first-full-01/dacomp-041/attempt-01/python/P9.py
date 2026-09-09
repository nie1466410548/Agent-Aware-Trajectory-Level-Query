import pandas as pd
import numpy as np

# Load display case data
high_case = pd.read_csv('/work/high_traffic_cases.csv')
print("=== DISPLAY CASE CONDITIONS (High Traffic) ===")
print("Seal status:")
print(high_case['Seal status'].value_counts())
print("\nMaintenance Status:")
print(high_case['Maintenance Status'].value_counts())
print("\nFilter status:")
print(high_case['Filter status'].value_counts())
print("\nSilica gel status:")
print(high_case['Silica gel status'].value_counts())
print("\nInert gas system status:")
print(high_case['Inert gas system status'].value_counts())
print("\nBackup system status:")
print(high_case['Backup system status'].value_counts())
print("\nPower status:")
print(high_case['Power status'].value_counts())
print("\nFire suppression system status:")
print(high_case['Fire suppression system status'].value_counts())
print("\nDisplay case material:")
print(high_case['Display case material'].value_counts())

print(f"\n=== Airtightness ===")
print(high_case['Airtightness'].describe())

print(f"\n=== Leak rate ===")
print(high_case['Leak rate'].describe())

print(f"\n=== Humidity buffering capacity ===")
print(high_case['Humidity buffering capacity'].describe())

print(f"\n=== Pollutant absorption capacity ===")
print(high_case['Pollutant absorption capacity'].describe())

# Compare with low-traffic
# Load all data
df_all_env = pd.read_csv('/work/all_env.csv')
low = df_all_env[df_all_env['Daily Visitor Count'] <= 900].copy()

# Same threshold exceedances for low traffic
print("\n\n=== THRESHOLD EXCEEDANCES COMPARISON ===")
for col, threshold, label in [
    ('Carbon dioxide concentration (ppm)', 800, 'CO2 > 800 ppm'),
    ('UV Irradiance (μW/cm²)', 75, 'UV > 75 μW/cm²'),
    ('\xa0Noise Level (dB)', 50, 'Noise > 50 dB'),
    ('\xa0Vibration Level (mm/s²)', 0.3, 'Vibration > 0.3 mm/s²'),
    ('PM2.5 concentration', 25, 'PM2.5 > 25 µg/m³'),
    ('Total volatile organic compounds concentration (ppb)', 300, 'TVOC > 300 ppb'),
    ('24-hour Temperature Change', 1.5, '24h Temp change > 1.5°C'),
    ('24-hour Humidity Change', 3, '24h RH change > 3%'),
    ('\xa0Mold Risk Index', 0.7, 'Mold Risk Index > 0.7'),
    ('\xa0Microbial Count (CFU)', 400, 'Microbial Count > 400 CFU'),
    ('Dust Accumulation (mg/m²)', 4, 'Dust > 4 mg/m²')
]:
    h_pct = (high[col] > threshold).sum() / len(high) * 100
    l_pct = (low[col] > threshold).sum() / len(low) * 100
    print(f"{label}: High={h_pct:.1f}%, Low={l_pct:.1f}%")

# Light sensitivity analysis
print("\n\n=== LIGHT SENSITIVITY OF ARTIFACTS IN HIGH TRAFFIC ===")
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
print("Light Sensitivity:")
print(high_art['Light Sensitivity'].value_counts())
print("\nTemperature Sensitivity:")
print(high_art['Temperature Sensitivity'].value_counts())
print("\nHumidity Sensitivity:")
print(high_art['Humidity Sensitivity'].value_counts())
print("\nVibration Sensitivity:")
print(high_art['Vibration Sensitivity'].value_counts())

# Cross-reference sensitive materials with environmental conditions
merged = pd.read_csv('/work/merged_high.csv')
print("\n\n=== LIGHT-SENSITIVE ITEMS (Paper, Textile) WITH HIGH ILLUMINANCE ===")
light_sensitive = merged[merged['Material Type'].isin(['Paper', 'Textile'])]
print(f"Total light-sensitive relics: {len(light_sensitive)}")
print(f"Avg illuminance on light-sensitive relics: {light_sensitive['\xa0Illuminance (Lux)'].mean():.1f} lux")
print(f"Avg UV on light-sensitive relics: {light_sensitive['UV Irradiance (μW/cm²)'].mean():.1f} μW/cm²")

# Material types with high deterioration rates
print("\n\n=== MATERIAL TYPES WITH HIGH DETERIORATION RATE (High Traffic) ===")
high_art['Material Type'] = merged['Material Type']
for mat in ['Paper', 'Textile', 'Wood', 'Bronze', 'Ceramic', 'Jade', 'Stone']:
    subset = merged[merged['Material Type'] == mat]
    if len(subset) > 0:
        rapid = (subset['Deterioration Rate'] == 'Rapid').sum()
        print(f"{mat}: {rapid}/{len(subset)} rapid deterioration ({rapid/len(subset)*100:.0f}%)")
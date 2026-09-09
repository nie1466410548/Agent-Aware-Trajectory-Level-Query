import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

NB = '\xa0'

# Load and clean all data
high = pd.read_csv('/work/high_traffic_env.csv')
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')
merged = pd.read_csv('/work/merged_high.csv')
df_risk = pd.read_csv('/work/high_traffic_risk.csv')
df_all = pd.read_csv('/work/all_env.csv')

# Strip whitespace from string columns
for df in [high_art, high_case, merged]:
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

print("========== COMPREHENSIVE RISK ANALYSIS ==========")
print(f"High-traffic exhibition halls (Daily Visitor Count > 900): {len(high)}")
print(f"Total halls in database: {len(df_all)}")

# === ENVIRONMENTAL RISKS ===
print("\n\n## 1. ENVIRONMENTAL RISK FACTORS")

# Air quality
print("\n### 1.1 Air Quality Concerns")
co2_high = (high['Carbon dioxide concentration (ppm)'] > 800).sum()
print(f"- Elevated CO2 (>800 ppm): {co2_high}/{len(high)} ({co2_high/len(high)*100:.1f}%)")
tvoc_high = (high['Total volatile organic compounds concentration (ppb)'] > 300).sum()
print(f"- Elevated TVOC (>300 ppb): {tvoc_high}/{len(high)} ({tvoc_high/len(high)*100:.1f}%)")
pm_high = (high['PM2.5 concentration'] > 25).sum()
print(f"- Elevated PM2.5 (>25 µg/m³): {pm_high}/{len(high)} ({pm_high/len(high)*100:.1f}%)")
pm10_high = (high['PM10 concentration'] > 35).sum()
print(f"- Elevated PM10 (>35 µg/m³): {pm10_high}/{len(high)} ({pm10_high/len(high)*100:.1f}%)")
form_high = (high['Formaldehyde concentration'] > 0.08).sum()
print(f"- Elevated Formaldehyde (>0.08): {form_high}/{len(high)} ({form_high/len(high)*100:.1f}%)")

# Temperature & Humidity
print("\n### 1.2 Temperature & Humidity Risks")
temp_high = (high['Temperature (°C)'] > 20).sum()
temp_low = (high['Temperature (°C)'] < 18).sum()
print(f"- Temperature out of range (18-20°C): {temp_high + temp_low}/{len(high)} ({((temp_high+temp_low)/len(high))*100:.1f}%)")
rh_high = (high['Relative Humidity (%)'] > 52).sum()
rh_low = (high['Relative Humidity (%)'] < 48).sum()
print(f"- RH out of range (48-52%): {rh_high + rh_low}/{len(high)} ({((rh_high+rh_low)/len(high))*100:.1f}%)")
tc_high = (high['24-hour Temperature Change'] > 1.5).sum()
print(f"- Large 24h temp fluctuation (>1.5°C): {tc_high}/{len(high)} ({tc_high/len(high)*100:.1f}%)")
rc_high = (high['24-hour Humidity Change'] > 3).sum()
print(f"- Large 24h RH fluctuation (>3%): {rc_high}/{len(high)} ({rc_high/len(high)*100:.1f}%)")

# Light & Radiation
print("\n### 1.3 Light & Radiation Risks")
illum_avg = high[NB+'Illuminance (Lux)'].mean()
print(f"- Average illuminance: {illum_avg:.1f} lux")
uv_avg = high['UV Irradiance (μW/cm²)'].mean()
print(f"- Average UV irradiance: {uv_avg:.1f} μW/cm²")
ir_avg = high[NB+'IR Irradiance (W/m²)'].mean()
print(f"- Average IR irradiance: {ir_avg:.1f} W/m²")
lux_high = (high[NB+'Illuminance (Lux)'] > 150).sum()
print(f"- Illuminance >150 lux (high for sensitive materials): {lux_high}/{len(high)} ({lux_high/len(high)*100:.1f}%)")

# Surface & Physical
print("\n### 1.4 Surface & Physical Risks")
vib_high = (high[NB+'Vibration Level (mm/s²)'] > 0.3).sum()
print(f"- High vibration (>0.3 mm/s²): {vib_high}/{len(high)} ({vib_high/len(high)*100:.1f}%)")
noise_high = (high[NB+'Noise Level (dB)'] > 50).sum()
print(f"- High noise (>50 dB): {noise_high}/{len(high)} ({noise_high/len(high)*100:.1f}%)")
dust_high = (high['Dust Accumulation (mg/m²)'] > 4).sum()
print(f"- High dust accumulation (>4 mg/m²): {dust_high}/{len(high)} ({dust_high/len(high)*100:.1f}%)")
microbe_high = (high[NB+'Microbial Count (CFU)'] > 400).sum()
print(f"- High microbial count (>400 CFU): {microbe_high}/{len(high)} ({microbe_high/len(high)*100:.1f}%)")
mold_high = (high[NB+'Mold Risk Index'] > 0.7).sum()
print(f"- High mold risk (>0.7): {mold_high}/{len(high)} ({mold_high/len(high)*100:.1f}%)")
corr_high = (high['Metal Corrosion Rate'] > 0.08).sum()
print(f"- High metal corrosion rate (>0.08): {corr_high}/{len(high)} ({corr_high/len(high)*100:.1f}%)")
org_high = (high['Organic Degradation Index'] > 0.7).sum()
print(f"- High organic degradation (>0.7): {org_high}/{len(high)} ({org_high/len(high)*100:.1f}%)")

# === ARTIFACT RISKS ===
print("\n\n## 2. ARTIFACT CONDITION & CONSERVATION RISKS")
print(f"\n### 2.1 Material Type Distribution")
print(high_art['Material Type'].value_counts().to_string())
print(f"\n### 2.2 Preservation Status")
print(high_art['Preservation Status'].value_counts().to_string())
print(f"\n### 2.3 Deterioration Rate")
print(high_art['Deterioration Rate'].value_counts().to_string())
print(f"\n### 2.4 Treatment Priority")
print(high_art['Treatment Priority'].value_counts().to_string())
print(f"\n### 2.5 Conservation Difficulty")
print(high_art['Conservation Difficulty'].value_counts().to_string())
print(f"\n### 2.6 Material Stability")
print(high_art['Material Stability'].value_counts().to_string())
print(f"\n### 2.7 Sensitivities")
print(f"Environmental Sensitivity: {high_art['Environmental Sensitivity'].value_counts().to_dict()}")
print(f"Light Sensitivity: {high_art['Light Sensitivity'].value_counts().to_dict()}")
print(f"Vibration Sensitivity: {high_art['Vibration Sensitivity'].value_counts().to_dict()}")
print(f"Humidity Sensitivity: {high_art['Humidity Sensitivity'].value_counts().to_dict()}")
print(f"Temperature Sensitivity: {high_art['Temperature Sensitivity'].value_counts().to_dict()}")

# === DISPLAY CASE RISKS ===
print("\n\n## 3. DISPLAY CASE INFRASTRUCTURE RISKS")
print(f"Seal status: {high_case['Seal status'].value_counts().to_dict()}")
print(f"Filter status: {high_case['Filter status'].value_counts().to_dict()}")
print(f"Silica gel status: {high_case['Silica gel status'].value_counts().to_dict()}")
print(f"Maintenance Status: {high_case['Maintenance Status'].value_counts().to_dict()}")
print(f"Avg Airtightness: {high_case['Airtightness'].mean():.1f}%")
print(f"Avg Leak rate: {high_case['Leak rate'].mean():.3f}")
print(f"Avg Humidity buffering capacity: {high_case['Humidity buffering capacity'].mean():.0f}")
print(f"Avg Pollutant absorption capacity: {high_case['Pollutant absorption capacity'].mean():.2f}")

# === RISK ASSESSMENT ===
print("\n\n## 4. FORMAL RISK ASSESSMENT")
print(f"Risk Levels: {df_risk['Risk Assessment Level'].value_counts().to_dict()}")
print(f"Conservation Priority Score - Mean: {df_risk['Conservation Priority Score'].mean():.0f}, " +
      f"High risk (score>60): {(df_risk['Conservation Priority Score'] > 60).sum()}/104 " +
      f"({(df_risk['Conservation Priority Score'] > 60).mean()*100:.1f}%)")

# Cross-reference high-risk combinations
print("\n\n## 5. HIGH-RISK COMBINATIONS")
# Paper/Textile with high light + high illuminance
light_sens = merged[merged['Material Type'].isin(['Paper', 'Textile'])]
print(f"Paper/Textile relics exposed to >150 lux: {(light_sens[NB+'Illuminance (Lux)'] > 150).sum()}/{len(light_sens)}")
print(f"Paper/Textile with high UV (>50 μW/cm²): {(light_sens['UV Irradiance (μW/cm²)'] > 50).sum()}/{len(light_sens)}")

# High vibration sensitivity + high vibration
vib_sens = merged[merged['Vibration Sensitivity'] == 'High']
if len(vib_sens) > 0:
    print(f"Vibration-sensitive relics with >0.3 mm/s²: {(vib_sens[NB+'Vibration Level (mm/s²)'] > 0.3).sum()}/{len(vib_sens)}")

# Poor condition + urgent priority
urgent = merged[merged['Treatment Priority'].isin(['Urgent', 'High'])]
print(f"Urgent/High priority relics with poor condition (<40): {(urgent['Condition Assessment Rating'] < 40).sum()}/{len(urgent)}")

# Maintenance overdue + poor seal
print(f"Maintenance overdue + poor seal: {(high_case['Maintenance Status'] == 'Overdue').sum()} overdue, " +
      f"{(high_case['Seal status'] == 'Poor').sum()} poor seal, " +
      f"{((high_case['Maintenance Status'] == 'Overdue') & (high_case['Seal status'] == 'Poor')).sum()} both")

# === COMPARISON WITH LOW TRAFFIC ===
print("\n\n## 6. COMPARISON: HIGH vs LOW TRAFFIC")
low = df_all[df_all['Daily Visitor Count'] <= 900]
for param, label in [
    ('Carbon dioxide concentration (ppm)', 'CO2 (ppm)'),
    ('PM2.5 concentration', 'PM2.5 (µg/m³)'),
    (NB+'Noise Level (dB)', 'Noise Level (dB)'),
    (NB+'Microbial Count (CFU)', 'Microbial Count (CFU)'),
    ('Dust Accumulation (mg/m²)', 'Dust (mg/m²)'),
    (NB+'Vibration Level (mm/s²)', 'Vibration (mm/s²)'),
    ('UV Irradiance (μW/cm²)', 'UV (μW/cm²)'),
    ('Total volatile organic compounds concentration (ppb)', 'TVOC (ppb)')
]:
    h_mean = high[param].mean()
    l_mean = low[param].mean()
    pct_diff = (h_mean - l_mean) / l_mean * 100
    print(f"  {label}: High={h_mean:.2f}, Low={l_mean:.2f}, Diff={pct_diff:+.1f}%")

print("\n\nAnalysis complete.")
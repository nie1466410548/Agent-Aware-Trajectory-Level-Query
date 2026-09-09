import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_all = pd.read_csv('/work/all_env.csv')
df_all_art = pd.read_csv('/work/all_artifacts.csv')

# Split into high-traffic (>900) and low-traffic (<=900)
high = df_all[df_all['Daily Visitor Count'] > 900].copy()
low = df_all[df_all['Daily Visitor Count'] <= 900].copy()

print(f"High-traffic halls: {len(high)}")
print(f"Low-traffic halls: {len(low)}")

# Compare environmental parameters
env_cols = ['Temperature (°C)', '24-hour Temperature Change', 'Relative Humidity (%)', 
            '24-hour Humidity Change', 'Atmospheric Pressure (hPa)',
            'Carbon dioxide concentration (ppm)', 'Total volatile organic compounds concentration (ppb)',
            'Ozone concentration (ppb)', 'Sulfur dioxide concentration (ppb)', 'Nitrogen dioxide concentration (ppb)',
            'PM2.5 concentration', 'PM10 concentration', 'Formaldehyde concentration',
            'Air exchange rate', 'Airflow velocity (m/s)']

light_cols = ['\xa0Illuminance (Lux)', 'UV Irradiance (μW/cm²)', '\xa0IR Irradiance (W/m²)', 'Visible Light Exposure (Lx·h)']
surface_cols = ['\xa0Vibration Level (mm/s²)', '\xa0Noise Level (dB)', 'Dust Accumulation (mg/m²)',
                '\xa0Microbial Count (CFU)', '\xa0Mold Risk Index', 'Metal Corrosion Rate',
                'Organic Degradation Index', '\xa0Color Change (ΔE)', 'Oxygen Concentration', '\xa0Nitrogen Concentration']

# Compute statistics
def compute_stats(df, label):
    stats = []
    for col in env_cols + light_cols + surface_cols:
        if col in df.columns:
            stats.append({'Parameter': col, 'Mean': df[col].mean(), 'Std': df[col].std(), 
                          'Min': df[col].min(), 'Max': df[col].max(), 'Group': label})
    return pd.DataFrame(stats)

high_stats = compute_stats(high, 'High Traffic (>900)')
low_stats = compute_stats(low, 'Low Traffic (≤900)')

# Comparative table
comparison = high_stats.merge(low_stats, on='Parameter', suffixes=('_High', '_Low'))
comparison['Difference'] = comparison['Mean_High'] - comparison['Mean_Low']
comparison['Pct_Diff'] = (comparison['Mean_High'] - comparison['Mean_Low']) / comparison['Mean_Low'] * 100

# Round for display
for c in comparison.columns:
    if c != 'Parameter':
        comparison[c] = comparison[c].round(2)

print("=== ENVIRONMENTAL COMPARISON: HIGH vs LOW TRAFFIC ===")
print(comparison.to_string())

comparison.to_csv('/work/comparison_stats.csv', index=False)
print("\nComparison saved.")
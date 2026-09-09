import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

NB = '\xa0'

# Load data
merged = pd.read_csv('/work/merged_high.csv')
high = pd.read_csv('/work/high_traffic_env.csv')
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')
df_all = pd.read_csv('/work/all_env.csv')

# 1. FIGURE 1: Key environmental parameter comparison: High vs Low traffic
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
high_sub = df_all[df_all['Daily Visitor Count'] > 900]
low_sub = df_all[df_all['Daily Visitor Count'] <= 900]

params = ['Carbon dioxide concentration (ppm)', 'PM2.5 concentration', 
          NB + 'Noise Level (dB)', NB + 'Microbial Count (CFU)', 
          'Dust Accumulation (mg/m²)', 'UV Irradiance (μW/cm²)']
titles = ['CO2 Concentration (ppm)', 'PM2.5 Concentration (µg/m³)', 
          'Noise Level (dB)', 'Microbial Count (CFU)', 
          'Dust Accumulation (mg/m²)', 'UV Irradiance (µW/cm²)']

for i, (ax, param, title) in enumerate(zip(axes.flatten(), params, titles)):
    ax.hist(high_sub[param].dropna(), bins=15, alpha=0.6, label='High Traffic (>900)', color='coral')
    ax.hist(low_sub[param].dropna(), bins=15, alpha=0.4, label='Low Traffic (≤900)', color='steelblue')
    ax.set_xlabel(title)
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=8)
    ax.set_title(title, fontsize=10)

plt.tight_layout()
plt.savefig('/work/figure1_env_comparison.png', dpi=150)
plt.close()

# 2. FIGURE 2: Heatmap of correlations
fig, ax = plt.subplots(figsize=(12, 6))
corr_cols = ['Daily Visitor Count', 'Carbon dioxide concentration (ppm)', 
             'PM2.5 concentration', NB + 'Noise Level (dB)', 
             NB + 'Microbial Count (CFU)', 'Dust Accumulation (mg/m²)',
             NB + 'Vibration Level (mm/s²)', 'UV Irradiance (μW/cm²)', 
             NB + 'IR Irradiance (W/m²)', 'Temperature (°C)', 'Relative Humidity (%)',
             '24-hour Temperature Change', '24-hour Humidity Change']
existing = [c for c in corr_cols if c in df_all.columns]
corr_matrix = df_all[existing].corr()
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, fmt='.2f', ax=ax, 
            xticklabels=[c.replace(NB, '') for c in corr_matrix.columns],
            yticklabels=[c.replace(NB, '') for c in corr_matrix.columns])
ax.set_title('Correlation Matrix: Environmental Parameters', fontsize=14)
plt.tight_layout()
plt.savefig('/work/figure2_correlation_heatmap.png', dpi=150)
plt.close()

# 3. FIGURE 3: Condition Assessment Rating distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
high_art_sub = pd.read_csv('/work/all_artifacts.csv')
high_cond = high_art_sub[high_art_sub['Daily Visitor Count'] > 900]['Condition Assessment Rating']
low_cond = high_art_sub[high_art_sub['Daily Visitor Count'] <= 900]['Condition Assessment Rating']

axes[0].hist(high_cond, bins=20, alpha=0.6, color='coral', label='High Traffic')
axes[0].hist(low_cond, bins=20, alpha=0.4, color='steelblue', label='Low Traffic')
axes[0].set_xlabel('Condition Assessment Rating')
axes[0].set_ylabel('Frequency')
axes[0].legend()
axes[0].set_title('Condition Assessment Rating Distribution')

# Preservation status distribution
pres_high = high_art_sub[high_art_sub['Daily Visitor Count'] > 900]['Preservation Status'].value_counts()
pres_low = high_art_sub[high_art_sub['Daily Visitor Count'] <= 900]['Preservation Status'].value_counts()
pres_df = pd.DataFrame({'High Traffic': pres_high, 'Low Traffic': pres_low})
pres_df.plot(kind='bar', ax=axes[1], color=['coral', 'steelblue'], alpha=0.8)
axes[1].set_title('Preservation Status Distribution')
axes[1].set_xlabel('Preservation Status')
axes[1].set_ylabel('Count')
axes[1].legend()
plt.tight_layout()
plt.savefig('/work/figure3_condition_analysis.png', dpi=150)
plt.close()

# 4. FIGURE 4: Material type breakdown with treatment priority
fig, ax = plt.subplots(figsize=(12, 6))
ct = pd.crosstab(merged['Material Type'], merged['Treatment Priority'])
ct.plot(kind='bar', stacked=True, ax=ax, colormap='RdYlGn_r')
ax.set_title('Treatment Priority by Material Type (High Traffic Halls)', fontsize=13)
ax.set_xlabel('Material Type')
ax.set_ylabel('Count')
ax.legend(title='Treatment Priority')
plt.tight_layout()
plt.savefig('/work/figure4_material_treatment.png', dpi=150)
plt.close()

# 5. FIGURE 5: Display case condition status
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
# Seal status
seal_counts = high_case['Seal status'].value_counts()
axes[0].pie(seal_counts.values, labels=seal_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'gold', 'lightblue', 'salmon'])
axes[0].set_title('Display Case Seal Status')

# Filter status
filter_counts = high_case['Filter status'].value_counts()
axes[1].pie(filter_counts.values, labels=filter_counts.index, autopct='%1.1f%%', colors=['salmon', 'gold', 'lightblue'])
axes[1].set_title('Display Case Filter Status')

# Silica gel status
sg_counts = high_case['Silica gel status'].value_counts()
axes[2].pie(sg_counts.values, labels=sg_counts.index, autopct='%1.1f%%', colors=['lightgreen', 'salmon', 'gold'])
axes[2].set_title('Silica Gel Status')

plt.tight_layout()
plt.savefig('/work/figure5_display_case.png', dpi=150)
plt.close()

print("All figures saved successfully.")
print(f"High traffic halls: {len(high)}")
print(f"High traffic artifacts: {len(high_art)}")
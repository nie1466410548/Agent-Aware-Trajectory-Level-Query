import json, numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows = []
with open('/results/S12.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=['Year','Surface_Supply','Groundwater_Supply','Surf_GW_Ratio','Urbanization_Rate'])
df = df.sort_values('Year').reset_index(drop=True)

# 1. Regression: Ratio = a + b*Urbanization
slope_r, intercept_r, r_val_r, p_val_r, se_r = stats.linregress(df['Urbanization_Rate'], df['Surf_GW_Ratio'])
print(f"Ratio = {intercept_r:.4f} + {slope_r:.4f} * Urbanization")
print(f"R-squared = {r_val_r**2:.4f}, p = {p_val_r:.4f}")

# 2. First-difference correlation
df['dRatio'] = df['Surf_GW_Ratio'].diff()
df['dUrban'] = df['Urbanization_Rate'].diff()
# Drop NaN first row
diff_df = df.dropna(subset=['dRatio','dUrban'])
r_d, p_d = stats.pearsonr(diff_df['dRatio'], diff_df['dUrban'])
print(f"\nFirst-difference Pearson corr(dRatio, dUrban) = {r_d:.4f}, p = {p_d:.4f}")

# 3. Groundwater decline quantification
print(f"\nGroundwater peak: {df['Groundwater_Supply'].max():.2f} in {df.loc[df['Groundwater_Supply'].idxmax(),'Year']}")
print(f"Groundwater 2018: {df.loc[df['Year']==2018,'Groundwater_Supply'].values[0]:.2f}")
print(f"Groundwater decline from peak: {df['Groundwater_Supply'].max() - df.loc[df['Year']==2018,'Groundwater_Supply'].values[0]:.2f}")
print(f"Groundwater 2013-2018 change: {df.loc[df['Year']==2018,'Groundwater_Supply'].values[0] - df.loc[df['Year']==2013,'Groundwater_Supply'].values[0]:.2f}")

# 4. Ratio change decomposition: % change from surface vs groundwater
ratio_start = df.loc[df['Year']==2005,'Surf_GW_Ratio'].values[0]
ratio_end = df.loc[df['Year']==2018,'Surf_GW_Ratio'].values[0]
surf_start = df.loc[df['Year']==2005,'Surface_Supply'].values[0]
ground_start = df.loc[df['Year']==2005,'Groundwater_Supply'].values[0]
surf_end = df.loc[df['Year']==2018,'Surface_Supply'].values[0]
ground_end = df.loc[df['Year']==2018,'Groundwater_Supply'].values[0]
print(f"\n2005: Surface={surf_start}, Groundwater={ground_start}, Ratio={ratio_start:.4f}")
print(f"2018: Surface={surf_end}, Groundwater={ground_end}, Ratio={ratio_end:.4f}")
print(f"Surface change: {surf_end-surf_start:.2f} ({(surf_end/surf_start-1)*100:.2f}%)")
print(f"Groundwater change: {ground_end-ground_start:.2f} ({(ground_end/ground_start-1)*100:.2f}%)")

# --- Figure 1: Dual-axis time series ---
fig, ax1 = plt.subplots(figsize=(10,5))
ax1.plot(df['Year'], df['Surf_GW_Ratio'], 'o-', color='#1f77b4', linewidth=2, markersize=6, label='Surface/Groundwater Ratio')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Surface-to-Groundwater Ratio', color='#1f77b4', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.axvspan(2014.5, 2018.5, alpha=0.08, color='blue', label='Acceleration phase')
ax1.set_xticks(df['Year'])
ax1.set_xticklabels(df['Year'], rotation=45)

ax2 = ax1.twinx()
ax2.plot(df['Year'], df['Urbanization_Rate'], 's--', color='#d62728', linewidth=2, markersize=6, label='Urbanization Rate (%)')
ax2.set_ylabel('Urbanization Rate (%)', color='#d62728', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#d62728')

# Add vertical lines at key years
for y in [2005, 2011, 2014, 2015, 2018]:
    ax1.axvline(x=y, color='grey', linestyle=':', alpha=0.4)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', fontsize=10)
ax1.set_title('China: Surface-to-Groundwater Ratio vs Urbanization Rate (2005-2018)', fontsize=13)
fig.tight_layout()
plt.savefig('/work/figure1_dual_axis.png', dpi=150)
plt.close()
print("Figure 1 saved: /work/figure1_dual_axis.png")

# --- Figure 2: Scatter plot with regression line ---
fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(df['Urbanization_Rate'], df['Surf_GW_Ratio'], c=df['Year'], cmap='viridis', s=80, zorder=5)
x_line = np.linspace(df['Urbanization_Rate'].min()-1, df['Urbanization_Rate'].max()+1, 100)
ax.plot(x_line, intercept_r + slope_r * x_line, 'r--', linewidth=2, label=f'Ratio = {intercept_r:.2f} + {slope_r:.2f}×Urban\nR²={r_val_r**2:.3f}')
# Label every other point
for i in range(0, len(df), 2):
    ax.annotate(int(df['Year'].iloc[i]), (df['Urbanization_Rate'].iloc[i], df['Surf_GW_Ratio'].iloc[i]),
                textcoords="offset points", xytext=(5,-5), fontsize=8)
ax.set_xlabel('Urbanization Rate (%)', fontsize=12)
ax.set_ylabel('Surface-to-Groundwater Ratio', fontsize=12)
ax.set_title('Surface-to-Groundwater Ratio vs Urbanization Rate (2005-2018)', fontsize=13)
ax.legend(fontsize=10)
fig.tight_layout()
plt.savefig('/work/figure2_scatter.png', dpi=150)
plt.close()
print("Figure 2 saved: /work/figure2_scatter.png")

# --- Figure 3: Components — Surface and Groundwater supply ---
fig, ax = plt.subplots(figsize=(10,5))
ax.fill_between(df['Year'], df['Groundwater_Supply'], alpha=0.3, color='orange', label='Groundwater')
ax.fill_between(df['Year'], df['Surface_Supply'], alpha=0.3, color='steelblue', label='Surface')
ax.plot(df['Year'], df['Surface_Supply'], 'o-', color='steelblue', linewidth=2, label='Surface Water Supply')
ax.plot(df['Year'], df['Groundwater_Supply'], 's-', color='darkorange', linewidth=2, label='Groundwater Supply')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Water Supply (100 million m³)', fontsize=12)
ax.set_title('China: Surface and Groundwater Supply Trends (2005-2018)', fontsize=13)
ax.set_xticks(df['Year'])
ax.set_xticklabels(df['Year'], rotation=45)
ax.legend(fontsize=10)
fig.tight_layout()
plt.savefig('/work/figure3_components.png', dpi=150)
plt.close()
print("Figure 3 saved: /work/figure3_components.png")
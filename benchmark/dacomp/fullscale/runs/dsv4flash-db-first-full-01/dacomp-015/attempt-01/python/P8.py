import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/parsed_data.csv')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12

# ========== FIGURE 1: Top 10 combinations by avg Watch Count ==========
# Load top 10 avg data
top10 = pd.read_csv('/work/top10_avg.csv')
top10['label'] = top10['Floor Plan'].str[:20] + ' | ' + top10['Decoration'].str[:10] + ' | ' + top10['Floor'].str[:10] + ' | ' + top10['Orientation']

fig, ax = plt.subplots(figsize=(15, 8))
colors = sns.color_palette('viridis', len(top10))
bars = ax.barh(range(len(top10)), top10['avg_watch'], color=colors)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(top10['label'], fontsize=10)
ax.set_xlabel('Average Watch Count', fontsize=14)
ax.set_title('Top 10 Home Combinations by Average Watch Count (cnt≥5)', fontsize=16, fontweight='bold')
ax.invert_yaxis()

# Add annotations
for i, (v, c) in enumerate(zip(top10['avg_watch'], top10['cnt'])):
    ax.text(v + 0.5, i, f'{v:.1f} (n={c})', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('/work/fig1_top10_combos.png', dpi=150)
plt.close()
print("fig1 saved")

# ========== FIGURE 2: Showings by factor ==========
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 2a: Showings by Decoration
dec_order = df.groupby('Decoration')['Showings'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Decoration', y='Showings', order=dec_order, ax=axes[0,0], palette='Blues_d')
axes[0,0].set_title('Average Showings by Decoration', fontweight='bold')
axes[0,0].tick_params(axis='x', rotation=45)

# 2b: Showings by Orientation
ori_order = df.groupby('Orientation')['Showings'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Orientation', y='Showings', order=ori_order, ax=axes[0,1], palette='Blues_d')
axes[0,1].set_title('Average Showings by Orientation', fontweight='bold')
axes[0,1].tick_params(axis='x', rotation=45)

# 2c: Showings by bedrooms
sns.barplot(data=df[df['bedrooms'].between(1,5)], x='bedrooms', y='Showings', ax=axes[0,2], palette='Blues_d')
axes[0,2].set_title('Average Showings by Bedrooms (1-5)', fontweight='bold')

# 2d: Showings by floor category
fc_order = df.groupby('floor_category')['Showings'].mean().sort_values(ascending=False).index
fc_order = [x for x in fc_order if x in ['low_floor','mid_floor','high_floor','building_total']]
sns.barplot(data=df[df['floor_category'].isin(fc_order)], x='floor_category', y='Showings', 
            order=fc_order, ax=axes[1,0], palette='Blues_d')
axes[1,0].set_title('Average Showings by Floor Category', fontweight='bold')
axes[1,0].tick_params(axis='x', rotation=45)

# 2e: Showings by Watch Count bin
df['watch_bin'] = pd.cut(df['Watch Count'], [-1,0,2,5,10,20,50,100,1000], 
                         labels=['0','1-2','3-5','6-10','11-20','21-50','51-100','100+'])
sns.barplot(data=df, x='watch_bin', y='Showings', ax=axes[1,1], palette='Reds_d')
axes[1,1].set_title('Average Showings by Watch Count Range', fontweight='bold')
axes[1,1].tick_params(axis='x', rotation=45)

# 2f: Regression coefficients for key factors
# From OLS results
coef_data = {
    'Watch Count': 0.043,
    'Floor Level': 0.036,
    'Bedrooms': 0.174,
    'Living Rooms': 0.393,
    'Area (sqm)': -0.013,
    'Price/sqm': 0.000036,
    'Dec: Simple Reno': 0.281,
    'Dec: Unfinished': 0.418,
    'Dec: Luxurious': -0.054,
    'Ori: South': 0.592,
}
coef_df = pd.DataFrame(list(coef_data.items()), columns=['Factor', 'Coefficient'])
coef_df = coef_df.sort_values('Coefficient')
colors = ['red' if c < 0 else 'green' for c in coef_df['Coefficient']]
axes[1,2].barh(coef_df['Factor'], coef_df['Coefficient'], color=colors)
axes[1,2].axvline(0, color='black', linewidth=0.5)
axes[1,2].set_title('OLS Regression Coefficients on Showings', fontweight='bold')
axes[1,2].set_xlabel('Coefficient')

plt.tight_layout()
plt.savefig('/work/fig2_showings_factors.png', dpi=150)
plt.close()
print("fig2 saved")

# ========== FIGURE 3: Watch Count by factors ==========
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 3a: Watch Count by Decoration
dec_order_w = df.groupby('Decoration')['Watch Count'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Decoration', y='Watch Count', order=dec_order_w, ax=axes[0,0], palette='Greens_d')
axes[0,0].set_title('Average Watch Count by Decoration', fontweight='bold')
axes[0,0].tick_params(axis='x', rotation=45)

# 3b: Watch Count by Orientation
ori_order_w = df.groupby('Orientation')['Watch Count'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Orientation', y='Watch Count', order=ori_order_w, ax=axes[0,1], palette='Greens_d')
axes[0,1].set_title('Average Watch Count by Orientation', fontweight='bold')
axes[0,1].tick_params(axis='x', rotation=45)

# 3c: Watch Count by bedrooms
sns.barplot(data=df[df['bedrooms'].between(1,5)], x='bedrooms', y='Watch Count', ax=axes[1,0], palette='Greens_d')
axes[1,0].set_title('Average Watch Count by Bedrooms (1-5)', fontweight='bold')

# 3d: Watch Count by floor category
sns.barplot(data=df[df['floor_category'].isin(['low_floor','mid_floor','high_floor','building_total'])], 
            x='floor_category', y='Watch Count', 
            order=['low_floor','mid_floor','high_floor','building_total'], ax=axes[1,1], palette='Greens_d')
axes[1,1].set_title('Average Watch Count by Floor Category', fontweight='bold')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/fig3_watch_factors.png', dpi=150)
plt.close()
print("fig3 saved")

# ========== FIGURE 4: Scatter - Watch Count vs Showings ==========
fig, ax = plt.subplots(figsize=(10, 8))
# Sample for plotting
sample = df.sample(min(5000, len(df)))
ax.scatter(sample['Watch Count'], sample['Showings'], alpha=0.3, s=10)
ax.set_xlabel('Watch Count', fontsize=14)
ax.set_ylabel('Showings', fontsize=14)
ax.set_title('Watch Count vs Showings (Sampled 5000 listings)', fontsize=16, fontweight='bold')

# Add trend line
z = np.polyfit(sample['Watch Count'], sample['Showings'], 1)
p = np.poly1d(z)
x_range = np.linspace(0, sample['Watch Count'].max(), 100)
ax.plot(x_range, p(x_range), 'r--', linewidth=2, label=f'Trend (slope={z[0]:.4f})')
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig4_watch_vs_showings.png', dpi=150)
plt.close()
print("fig4 saved")

print("All figures saved.")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load data
rows = db.query("""
  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome
""")
df = db.frame(rows)

def parse_price(s):
    if pd.isna(s): return None
    s = str(s).replace(',', '').replace(' yuan', '').replace(' (variant)', '').replace(' (no space)', '').replace(' (with space)', '').replace(' yuan ', '').strip()
    try: return float(s)
    except: return None

def parse_mileage(s):
    if pd.isna(s): return None
    s = str(s)
    if 'ten thousand km' in s:
        try: return float(s.replace(' ten thousand km', '')) * 10000
        except: return None
    elif 'km' in s:
        try: return float(s.replace(',', '').replace(' km', ''))
        except: return None
    return None

def parse_owners(s):
    if pd.isna(s): return None
    try: return int(str(s)[0])
    except: return None

df['np_yuan'] = df['np_raw'].apply(parse_price)
df['mileage_km'] = df['Mileage'].apply(parse_mileage)
df['owners'] = df['Number of Previous Owners'].apply(parse_owners)
df['Posting Date'] = df['Posting Date'].astype(str).str.strip()
df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce')
df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')
df['age_years'] = (df['Posting Date'] - df['Registration Date']).dt.days / 365.25
df['retention'] = df['Price'] * 10000 / df['np_yuan']

# Clean data
expensive_keywords = ['Mercedes', 'BMW iX', 'Cadillac', 'Gaohe', 'Zeekr', 'Weilai', 'ET7', 'Li Xiang', 'L9', 'L8', 'L7', 'Xpeng G9', 'HiPhi', 'Tesla Model Y', 'Tang', 'Deep Blue', 'Avita', 'LYRIQ', 'Volvo', 'Porsche', 'Audi', 'Polestar', 'IM L7', 'Lantu', 'Dengshi', 'D9', 'Jaguar', 'Hongqi']
df['has_expensive_title'] = df['Title'].str.contains('|'.join(expensive_keywords), case=False, na=False)
df['is_clean'] = ~(df['has_expensive_title'] & (df['np_yuan'] < 150000))
df_clean = df[df['is_clean']].copy()

print(f"Clean rows: {len(df_clean)}")

# === FIGURE 1: Overall analysis ===
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Retention histogram
axes[0,0].hist(df_clean['retention']*100, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0,0].axvline(df_clean['retention'].mean()*100, color='red', linestyle='--', linewidth=2, label=f'Mean: {df_clean["retention"].mean()*100:.1f}%')
axes[0,0].set_xlabel('Retention Rate (%)')
axes[0,0].set_ylabel('Count')
axes[0,0].set_title(f'Used Car Retention Rate Distribution (n={len(df_clean)})')
axes[0,0].legend()

# 2. Retention by Fuel Type
fuel_grp = df_clean.groupby('Fuel Type')['retention'].agg(['mean', 'count', 'std'])
colors = ['#2ecc71', '#3498db', '#e74c3c']
axes[0,1].bar(range(len(fuel_grp)), fuel_grp['mean']*100, yerr=fuel_grp['std']*100, capsize=5, alpha=0.7, color=colors[:len(fuel_grp)])
axes[0,1].set_xticks(range(len(fuel_grp)))
axes[0,1].set_xticklabels(fuel_grp.index)
axes[0,1].set_ylabel('Avg Retention Rate (%)')
axes[0,1].set_title('Retention by Fuel Type')
for i, (idx, row) in enumerate(fuel_grp.iterrows()):
    axes[0,1].text(i, row['mean']*100+1, f'n={int(row["count"])}', ha='center', fontsize=10)

# 3. Retention vs Age
idx_valid = df_clean['age_years'].notna() & df_clean['retention'].notna()
sc = axes[0,2].scatter(df_clean.loc[idx_valid, 'age_years'], df_clean.loc[idx_valid, 'retention']*100, 
                       c=df_clean.loc[idx_valid, 'np_yuan']/10000, cmap='viridis', alpha=0.5, s=15)
axes[0,2].set_xlabel('Vehicle Age (years)')
axes[0,2].set_ylabel('Retention Rate (%)')
axes[0,2].set_title('Retention vs Age (color = new car price)')
plt.colorbar(sc, ax=axes[0,2], label='New Car Price (万元)')
z = np.polyfit(df_clean.loc[idx_valid, 'age_years'], df_clean.loc[idx_valid, 'retention']*100, 1)
p = np.poly1d(z)
x_line = np.linspace(df_clean.loc[idx_valid, 'age_years'].min(), df_clean.loc[idx_valid, 'age_years'].max(), 100)
axes[0,2].plot(x_line, p(x_line), 'r--', linewidth=2, label=f'y={z[0]:.1f}x+{z[1]:.1f}')
axes[0,2].legend()

# 4. Retention by Vehicle Class (top)
vc = df_clean.groupby('Vehicle Class')['retention'].agg(['mean', 'count']).sort_values('mean', ascending=False)
vc_top = vc[vc['count'] >= 3]
axes[1,0].barh(range(len(vc_top)), vc_top['mean']*100, alpha=0.7, color='steelblue')
axes[1,0].set_yticks(range(len(vc_top)))
axes[1,0].set_yticklabels(vc_top.index)
axes[1,0].invert_yaxis()
axes[1,0].set_xlabel('Avg Retention Rate (%)')
axes[1,0].set_title('Retention by Vehicle Class (n>=3)')
for i, (idx, row) in enumerate(vc_top.iterrows()):
    axes[1,0].text(row['mean']*100+0.5, i, f'{row["mean"]*100:.1f}% (n={int(row["count"])})', va='center', fontsize=9)

# 5. Retention by Owners
owners_grp = df_clean.groupby('owners')['retention'].agg(['mean', 'count', 'std'])
axes[1,1].bar(range(len(owners_grp)), owners_grp['mean']*100, yerr=owners_grp['std']*100, capsize=5, alpha=0.7, color='#2ecc71')
axes[1,1].set_xticks(range(len(owners_grp)))
axes[1,1].set_xticklabels([str(int(x)) for x in owners_grp.index])
axes[1,1].set_xlabel('Number of Previous Owners')
axes[1,1].set_ylabel('Avg Retention Rate (%)')
axes[1,1].set_title('Retention by Ownership History')
for i, (idx, row) in enumerate(owners_grp.iterrows()):
    axes[1,1].text(i, row['mean']*100+1, f'n={int(row["count"])}', ha='center', fontsize=10)

# 6. Retention by Tags
tags_grp = df_clean.groupby('Tags')['retention'].agg(['mean', 'count']).sort_values('mean', ascending=False)
tags_grp_top = tags_grp[tags_grp['count'] >= 3].head(8)
axes[1,2].barh(range(len(tags_grp_top)), tags_grp_top['mean']*100, alpha=0.7, color='coral')
axes[1,2].set_yticks(range(len(tags_grp_top)))
axes[1,2].set_yticklabels(tags_grp_top.index)
axes[1,2].invert_yaxis()
axes[1,2].set_xlabel('Avg Retention Rate (%)')
axes[1,2].set_title('Retention by Listing Tags (n>=3)')
for i, (idx, row) in enumerate(tags_grp_top.iterrows()):
    axes[1,2].text(row['mean']*100+0.5, i, f'{row["mean"]*100:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/figure1_detailed_analysis.png', dpi=150)
plt.close()
print("Figure 1 saved.")

# === FIGURE 2: Top models by retention (clean data, n>=3) ===
model_stats = df_clean.groupby('Title').agg(
    avg_retention=('retention', 'mean'),
    count=('retention', 'count'),
    avg_age=('age_years', 'mean'),
    avg_price=('Price', 'mean'),
    avg_mileage=('mileage_km', 'mean')
).reset_index()
model_stats['avg_retention_pct'] = model_stats['avg_retention'] * 100
model_stats_f = model_stats[model_stats['count'] >= 3].sort_values('avg_retention', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(18, 10))

# Top models
top = model_stats_f.head(12)
bars1 = axes[0].barh(range(len(top)), top['avg_retention_pct'], alpha=0.7, color='steelblue')
axes[0].set_yticks(range(len(top)))
axes[0].set_yticklabels(top['Title'], fontsize=9)
axes[0].invert_yaxis()
axes[0].set_xlabel('Avg Retention Rate (%)')
axes[0].set_xlim(0, 90)
axes[0].set_title('Top 12 Models by Retention Rate (n>=3, clean data)')
for i, (_, row) in enumerate(top.iterrows()):
    axes[0].text(row['avg_retention_pct']+1, i, f'{row["avg_retention_pct"]:.1f}% (n={int(row["count"])}, '
                f'{row["avg_age"]:.1f}y)', va='center', fontsize=8)

# Bottom models
bottom = model_stats_f.tail(8)
bars2 = axes[1].barh(range(len(bottom)), bottom['avg_retention_pct'], alpha=0.7, color='coral')
axes[1].set_yticks(range(len(bottom)))
axes[1].set_yticklabels(bottom['Title'], fontsize=9)
axes[1].invert_yaxis()
axes[1].set_xlabel('Avg Retention Rate (%)')
axes[1].set_xlim(0, 90)
axes[1].set_title('Bottom 8 Models by Retention Rate (n>=3, clean data)')
for i, (_, row) in enumerate(bottom.iterrows()):
    axes[1].text(row['avg_retention_pct']+1, i, f'{row["avg_retention_pct"]:.1f}% (n={int(row["count"])}, '
                f'{row["avg_age"]:.1f}y)', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('/work/figure2_model_ranking.png', dpi=150)
plt.close()
print("Figure 2 saved.")

# === FIGURE 3: Premium model retention (clean, >=30万) ===
premium = df[(df['np_yuan'] >= 300000) & (df['is_clean'])].copy()
premium_sorted = premium.sort_values('retention', ascending=False)

fig, ax = plt.subplots(figsize=(14, 8))
premium_plot = premium_sorted.copy()
premium_plot['label'] = premium_plot['Title'].str[:45]
bars = ax.barh(range(len(premium_plot)), premium_plot['retention']*100, alpha=0.7)
for i, (_, row) in enumerate(premium_plot.iterrows()):
    if row['age_years'] < 1:
        bars[i].set_color('#2ecc71')
    elif row['age_years'] < 2:
        bars[i].set_color('#3498db')
    elif row['age_years'] < 3:
        bars[i].set_color('#f39c12')
    else:
        bars[i].set_color('#e74c3c')

ax.set_yticks(range(len(premium_plot)))
ax.set_yticklabels(premium_plot['label'])
ax.invert_yaxis()
ax.set_xlabel('Retention Rate (%)')
ax.set_title(f'Premium Vehicle Retention Rates (>=30万 new, n={len(premium_plot)})')
ax.set_xlim(0, 100)
for i, (_, row) in enumerate(premium_plot.iterrows()):
    ax.text(row['retention']*100+1, i, f'{row["retention"]*100:.1f}% | {row["age_years"]:.1f}y | {row["mileage_km"]/10000:.1f}万km', 
            va='center', fontsize=8)

legend_elements = [Patch(facecolor='#2ecc71', label='< 1 year'),
                   Patch(facecolor='#3498db', label='1-2 years'),
                   Patch(facecolor='#f39c12', label='2-3 years'),
                   Patch(facecolor='#e74c3c', label='> 3 years')]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig('/work/figure3_premium_retention.png', dpi=150)
plt.close()
print("Figure 3 saved.")

# Print summary stats
print(f"\nOverall avg retention (clean): {df_clean['retention'].mean()*100:.1f}%")

# Best retention trims
elite = df_clean[df_clean['Title'].str.contains('Elite', case=False)]
standard = df_clean[df_clean['Title'].str.contains('Standard', case=False)]
luxury = df_clean[df_clean['Title'].str.contains('Luxury', case=False)]
print(f"Elite Edition: {elite['retention'].mean()*100:.1f}% (n={len(elite)})")
print(f"Standard Edition: {standard['retention'].mean()*100:.1f}% (n={len(standard)})")
print(f"Luxury Edition: {luxury['retention'].mean()*100:.1f}% (n={len(luxury)})")

# Best models by age-adjusted retention
print("\n=== TOP MODELS (age-adjusted) ===")
age_valid = df_clean[df_clean['age_years'].notna() & (df_clean['age_years'] > 0.5)]
age_valid['ret_per_year'] = age_valid['retention'] / age_valid['age_years']
model_yr = age_valid.groupby('Title').agg(
    avg_ret_per_yr=('ret_per_year', 'mean'),
    count=('ret_per_year', 'count'),
    avg_age=('age_years', 'mean')
).reset_index()
model_yr_f = model_yr[model_yr['count'] >= 2].sort_values('avg_ret_per_yr', ascending=False)
for _, row in model_yr_f.head(10).iterrows():
    print(f"{row['Title']:50s} {row['avg_ret_per_yr']*100:.1f}%/yr  age={row['avg_age']:.1f}y  n={int(row['count'])}")
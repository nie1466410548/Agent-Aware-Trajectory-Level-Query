import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Load the full data
rows = db.query("""
  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome
""")
df = db.frame(rows)

# Parse new car price
def parse_price(s):
    if pd.isna(s):
        return None
    s = str(s)
    s = s.replace(',', '').replace(' yuan', '').replace(' (variant)', '').replace(' (no space)', '').replace(' (with space)', '').replace(' yuan ', '').strip()
    try:
        return float(s)
    except:
        return None

df['np_yuan'] = df['np_raw'].apply(parse_price)

# Parse mileage
def parse_mileage(s):
    if pd.isna(s):
        return None
    s = str(s)
    if 'ten thousand km' in s:
        try:
            return float(s.replace(' ten thousand km', '')) * 10000
        except:
            return None
    elif 'km' in s:
        try:
            return float(s.replace(',', '').replace(' km', ''))
        except:
            return None
    return None

df['mileage_km'] = df['Mileage'].apply(parse_mileage)

# Parse dates
df['Posting Date'] = df['Posting Date'].astype(str).str.strip()
df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce')
df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')

# Compute age
df['age_years'] = (df['Posting Date'] - df['Registration Date']).dt.days / 365.25

# Compute retention
df['retention'] = df['Price'] * 10000 / df['np_yuan']

# Parse owners
def parse_owners(s):
    if pd.isna(s):
        return None
    try:
        return int(str(s)[0])
    except:
        return None

df['owners'] = df['Number of Previous Owners'].apply(parse_owners)

# Clean transmission and drivetrain
df['Transmission_clean'] = df['Transmission'].astype(str).str.strip().str.replace(' (with leading space)', '', regex=False).str.replace(' (with space)', '', regex=False)
df['Drivetrain_clean'] = df['Drivetrain'].astype(str).str.strip().str.replace(' (with space)', '', regex=False).str.replace('Front-engine, front-wheel drive', 'Front-engine Front-wheel Drive', regex=False)

# Extract model base name (first 2-3 words)
df['model_base'] = df['Title'].str.extract(r'^([\w\s]+?)\s+\d{4}', expand=False).str.strip()

print(f"Total rows: {len(df)}")
print(f"Rows with valid retention: {df['retention'].notna().sum()}")
print(f"Avg retention: {df['retention'].mean():.2%}")
print(f"Min retention: {df['retention'].min():.2%}")
print(f"Max retention: {df['retention'].max():.2%}")

# 1. FIGURE 1: Retention distribution histogram
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Histogram
axes[0,0].hist(df['retention']*100, bins=30, edgecolor='black', alpha=0.7)
axes[0,0].set_xlabel('Retention Rate (%)')
axes[0,0].set_ylabel('Count')
axes[0,0].set_title('Distribution of Vehicle Retention Rates')
axes[0,0].axvline(df['retention'].mean()*100, color='r', linestyle='--', label=f'Mean: {df["retention"].mean()*100:.1f}%')
axes[0,0].legend()

# Retention by Fuel Type
fuel_means = df.groupby('Fuel Type')['retention'].mean()*100
fuel_std = df.groupby('Fuel Type')['retention'].std()*100
fuel_counts = df.groupby('Fuel Type').size()
x = range(len(fuel_means))
axes[0,1].bar(x, fuel_means.values, yerr=fuel_std.values, capsize=5, alpha=0.7)
axes[0,1].set_xticks(x)
axes[0,1].set_xticklabels(fuel_means.index)
axes[0,1].set_ylabel('Avg Retention Rate (%)')
axes[0,1].set_title('Retention Rate by Fuel Type')
for i, (idx, val) in enumerate(fuel_means.items()):
    axes[0,1].text(i, val+1, f'n={fuel_counts[idx]}', ha='center', fontsize=9)

# Retention by Vehicle Class (top 8)
vc = df.groupby('Vehicle Class')['retention'].agg(['mean', 'count']).sort_values('mean', ascending=False)
vc_top = vc[vc['count'] >= 3]
x = range(len(vc_top))
axes[1,0].bar(x, vc_top['mean']*100, alpha=0.7)
axes[1,0].set_xticks(x)
axes[1,0].set_xticklabels(vc_top.index, rotation=45, ha='right')
axes[1,0].set_ylabel('Avg Retention Rate (%)')
axes[1,0].set_title('Retention Rate by Vehicle Class (n>=3)')

# Retention vs Age
axes[1,1].scatter(df['age_years'], df['retention']*100, alpha=0.3, s=10)
axes[1,1].set_xlabel('Vehicle Age (years)')
axes[1,1].set_ylabel('Retention Rate (%)')
axes[1,1].set_title('Retention Rate vs Vehicle Age')
# Add trend line
idx_valid = df['age_years'].notna() & df['retention'].notna()
if idx_valid.sum() > 0:
    z = np.polyfit(df.loc[idx_valid, 'age_years'], df.loc[idx_valid, 'retention']*100, 1)
    p = np.poly1d(z)
    x_line = np.linspace(df.loc[idx_valid, 'age_years'].min(), df.loc[idx_valid, 'age_years'].max(), 100)
    axes[1,1].plot(x_line, p(x_line), 'r--', linewidth=2)

plt.tight_layout()
plt.savefig('/work/figure1_overview.png', dpi=150)
plt.close()
print("Figure 1 saved.")

# 2. FIGURE 2: Top and Bottom models
model_stats = df.groupby('Title').agg(
    avg_retention=('retention', 'mean'),
    count=('retention', 'count'),
    avg_age=('age_years', 'mean'),
    avg_price=('Price', 'mean')
).reset_index()
model_stats['avg_retention_pct'] = model_stats['avg_retention'] * 100

# Filter models with >=3 listings
model_stats_f = model_stats[model_stats['count'] >= 3].sort_values('avg_retention', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Top 10
top10 = model_stats_f.head(10)
bars1 = axes[0].barh(range(len(top10)), top10['avg_retention_pct'].values, alpha=0.7)
axes[0].set_yticks(range(len(top10)))
axes[0].set_yticklabels(top10['Title'].values)
axes[0].invert_yaxis()
axes[0].set_xlabel('Avg Retention Rate (%)')
axes[0].set_title('Top 10 Models by Retention Rate (n>=3)')
for i, (idx, row) in enumerate(top10.iterrows()):
    axes[0].text(row['avg_retention_pct']+0.5, i, f'{row["avg_retention_pct"]:.1f}% (n={int(row["count"])})', va='center', fontsize=9)

# Bottom 10
bottom10 = model_stats_f.tail(10)
bars2 = axes[1].barh(range(len(bottom10)), bottom10['avg_retention_pct'].values, alpha=0.7, color='coral')
axes[1].set_yticks(range(len(bottom10)))
axes[1].set_yticklabels(bottom10['Title'].values)
axes[1].invert_yaxis()
axes[1].set_xlabel('Avg Retention Rate (%)')
axes[1].set_title('Bottom 10 Models by Retention Rate (n>=3)')
for i, (idx, row) in enumerate(bottom10.iterrows()):
    axes[1].text(row['avg_retention_pct']+0.5, i, f'{row["avg_retention_pct"]:.1f}% (n={int(row["count"])})', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/figure2_top_bottom_models.png', dpi=150)
plt.close()
print("Figure 2 saved.")

# Print model stats
print("\n--- Top 15 Models by Retention (n>=3) ---")
for _, row in model_stats_f.head(15).iterrows():
    print(f"{row['Title']:50s} {row['avg_retention_pct']:.1f}%  age={row['avg_age']:.2f}y  n={int(row['count'])}")

print("\n--- Bottom 15 Models by Retention (n>=3) ---")
for _, row in model_stats_f.tail(15).iterrows():
    print(f"{row['Title']:50s} {row['avg_retention_pct']:.1f}%  age={row['avg_age']:.2f}y  n={int(row['count'])}")
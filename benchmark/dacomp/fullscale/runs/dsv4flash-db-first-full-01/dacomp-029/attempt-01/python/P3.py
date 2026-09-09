import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Parse
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

df['np_yuan'] = df['np_raw'].apply(parse_price)
df['mileage_km'] = df['Mileage'].apply(parse_mileage)
df['Posting Date'] = df['Posting Date'].astype(str).str.strip()
df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce')
df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')
df['age_years'] = (df['Posting Date'] - df['Registration Date']).dt.days / 365.25
df['retention'] = df['Price'] * 10000 / df['np_yuan']

def parse_owners(s):
    if pd.isna(s): return None
    try: return int(str(s)[0])
    except: return None
df['owners'] = df['Number of Previous Owners'].apply(parse_owners)

# Model base
df['model_base'] = df['Title'].str.extract(r'^([\w\s]+?)\s+\d{4}', expand=False).str.strip()

# Count models with >=3
model_counts = df.groupby('Title').size()
print(f"Total distinct models: {len(model_counts)}")
print(f"Models with >=3 listings: {(model_counts >= 3).sum()}")
print(f"Models with >=5 listings: {(model_counts >= 5).sum()}")

# Analysis by model base
base_stats = df.groupby('model_base').agg(
    avg_retention=('retention', 'mean'),
    count=('retention', 'count'),
    avg_age=('age_years', 'mean'),
    avg_price=('Price', 'mean')
).reset_index()
base_stats['avg_retention_pct'] = base_stats['avg_retention'] * 100
base_stats_f = base_stats[base_stats['count'] >= 3].sort_values('avg_retention', ascending=False)

print(f"\n--- Top 10 Model Bases by Retention (n>=3) ---")
for _, row in base_stats_f.head(10).iterrows():
    print(f"{row['model_base']:40s} {row['avg_retention_pct']:.1f}%  age={row['avg_age']:.2f}y  n={int(row['count'])}")

print(f"\n--- Bottom 10 Model Bases by Retention (n>=3) ---")
for _, row in base_stats_f.tail(10).iterrows():
    print(f"{row['model_base']:40s} {row['avg_retention_pct']:.1f}%  age={row['avg_age']:.2f}y  n={int(row['count'])}")

# Now create figure 3: Age-adjusted retention analysis
# Compute age-normalized retention (retention per year of age)
df_valid = df[df['age_years'].notna() & df['retention'].notna()].copy()
df_valid['retention_per_year'] = df_valid['retention'] / df_valid['age_years']

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. Retention vs Mileage
axes[0].scatter(df_valid['mileage_km']/10000, df_valid['retention']*100, alpha=0.3, s=10)
axes[0].set_xlabel('Mileage (ten thousand km)')
axes[0].set_ylabel('Retention Rate (%)')
axes[0].set_title('Retention Rate vs Mileage')

# 2. Retention by number of owners
owners_stats = df.groupby('owners')['retention'].agg(['mean', 'count', 'std'])
axes[1].bar(owners_stats.index, owners_stats['mean']*100, yerr=owners_stats['std']*100, capsize=5, alpha=0.7)
axes[1].set_xlabel('Number of Previous Owners')
axes[1].set_ylabel('Avg Retention Rate (%)')
axes[1].set_title('Retention Rate by Number of Owners')
for idx, row in owners_stats.iterrows():
    axes[1].text(idx, row['mean']*100+1, f'n={int(row["count"])}', ha='center', fontsize=9)

# 3. Retention per year by model base (top)
base_yr = df_valid.groupby('model_base').agg(
    avg_ret_per_yr=('retention_per_year', 'mean'),
    count=('retention_per_year', 'count')
).reset_index()
base_yr_f = base_yr[base_yr['count'] >= 3].sort_values('avg_ret_per_yr', ascending=False)

top10_yr = base_yr_f.head(10)
bars = axes[2].barh(range(len(top10_yr)), top10_yr['avg_ret_per_yr'].values, alpha=0.7)
axes[2].set_yticks(range(len(top10_yr)))
axes[2].set_yticklabels(top10_yr['model_base'].values)
axes[2].invert_yaxis()
axes[2].set_xlabel('Retention Rate per Year (%)')
axes[2].set_title('Top 10 Model Bases: Annual Retention Rate (n>=3)')
for i, (_, row) in enumerate(top10_yr.iterrows()):
    axes[2].text(row['avg_ret_per_yr']+0.5, i, f'{row["avg_ret_per_yr"]:.1f}%/y (n={int(row["count"])})', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/figure3_age_adjusted_analysis.png', dpi=150)
plt.close()
print("Figure 3 saved.")

# Color analysis (group similar colors)
color_map = {
    'White': 'White', 'Pearl White': 'White', 'Ivory White': 'White', 'Cream White': 'White',
    'Black': 'Black', 'Carbon Black': 'Black',
    'Silver/gray': 'Silver/Gray', 'Gray': 'Silver/Gray', 'Silver': 'Silver/Gray', 'Grey': 'Silver/Gray',
    'Blue': 'Blue', 'Sky Blue': 'Blue', 'Dark Blue': 'Blue', 'Mint Cyan': 'Blue',
    'Red': 'Red', 'Red/Purple': 'Red', 'Strawberry Red': 'Red',
    'Green': 'Green', 'Mint Green': 'Green', 'Grass Green': 'Green',
    'Pink': 'Pink', 'Rose Pink': 'Pink',
    'Yellow': 'Yellow', 'Mango Yellow': 'Yellow',
    'Purple': 'Purple', 'Violet': 'Purple',
    'Brown': 'Brown', 'Chocolate Color': 'Brown',
    'Orange': 'Orange',
    'Gold': 'Gold',
    'Cyan': 'Cyan', 'Tiffany blue': 'Cyan',
    'Milk Tea Color': 'Other',
}

def simplify_color(c):
    if pd.isna(c): return 'Unknown'
    c = str(c).strip()
    for key, val in color_map.items():
        if key in c:
            return val
    if c in color_map:
        return color_map[c]
    return 'Other'

df['color_simple'] = df['Color'].apply(simplify_color)
color_stats = df.groupby('color_simple')['retention'].agg(['mean', 'count', 'std']).sort_values('mean', ascending=False)
print("\n--- Retention by Color Group ---")
for idx, row in color_stats.iterrows():
    print(f"{idx:20s} {row['mean']*100:.1f}%  n={int(row['count'])}")

# Model base avg age
base_age = df.groupby('model_base')['age_years'].mean().sort_values()
print("\n--- Distinct model bases ---")
print(sorted(df['model_base'].dropna().unique()))

# Full model stats with age
model_stats = df.groupby('Title').agg(
    avg_retention=('retention', 'mean'),
    count=('retention', 'count'),
    avg_age=('age_years', 'mean'),
    avg_price=('Price', 'mean'),
    avg_mileage=('mileage_km', 'mean')
).reset_index()
model_stats['avg_retention_pct'] = model_stats['avg_retention'] * 100
model_stats_f = model_stats[model_stats['count'] >= 3].sort_values('avg_retention', ascending=False)

print(f"\n--- All models with n>=3 ({len(model_stats_f)} models) ---")
for _, row in model_stats_f.iterrows():
    print(f"{row['Title']:55s} {row['avg_retention_pct']:.1f}%  age={row['avg_age']:.2f}y  mileage={row['avg_mileage']/10000:.1f}万km  n={int(row['count'])}")
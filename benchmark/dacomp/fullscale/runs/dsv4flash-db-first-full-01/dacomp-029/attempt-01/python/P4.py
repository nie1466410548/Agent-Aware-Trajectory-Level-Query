import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df['np_yuan'] = df['np_raw'].apply(parse_price)
df['mileage_km'] = df['Mileage'].apply(parse_mileage)
df['Posting Date'] = df['Posting Date'].astype(str).str.strip()
df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce')
df['Posting Date'] = pd.to_datetime(df['Posting Date'], errors='coerce')
df['age_years'] = (df['Posting Date'] - df['Registration Date']).dt.days / 365.25
df['retention'] = df['Price'] * 10000 / df['np_yuan']
df['model_base'] = df['Title'].str.extract(r'^([\w\s]+?)\s+\d{4}', expand=False).str.strip()

# Luxury brands
luxury_keywords = ['Audi', 'BMW', 'Mercedes', 'Porsche', 'Cayenne', 'Cadillac', 'Volvo', 'Polestar', 'Lexus']
df['is_luxury'] = df['model_base'].apply(lambda x: any(k in str(x) for k in luxury_keywords))

print("=== LUXURY/PRESTIGE VEHICLES ===")
luxury = df[df['is_luxury']].copy()
print(f"Count: {len(luxury)}")
for _, row in luxury.iterrows():
    print(f"  {row['Title']:55s} Price={row['Price']:8.2f}万  New={row['np_yuan']:>8.0f}元  Retention={row['retention']*100:5.1f}%  Age={row['age_years']:.2f}y  Mileage={row['mileage_km']/10000:.1f}万km")

# Tag analysis
print("\n=== TAG ANALYSIS ===")
tag_groups = df.groupby('Tags')['retention'].agg(['mean', 'count', 'std']).sort_values('mean', ascending=False)
for idx, row in tag_groups.iterrows():
    if row['count'] >= 3:
        print(f"{str(idx):50s} {row['mean']*100:5.1f}%  n={int(row['count'])}")

# Models with highest retention regardless of model count
print("\n=== TOP 20 INDIVIDUAL LISTINGS by Retention ===")
df_sorted = df.sort_values('retention', ascending=False)
for _, row in df_sorted.head(20).iterrows():
    print(f"{row['Title']:55s} Retention={row['retention']*100:5.1f}%  Price={row['Price']:6.2f}万  Age={row['age_years']:.2f}y  Mileage={row['mileage_km']/10000:.1f}万km  Fuel={row['Fuel Type']}")

# Average retention by price segment
print("\n=== RETENTION BY PRICE SEGMENT ===")
df['price_segment'] = pd.cut(df['np_yuan'], bins=[0, 80000, 150000, 300000, 500000, 10000000], 
                             labels=['<8万', '8-15万', '15-30万', '30-50万', '>50万'])
seg_stats = df.groupby('price_segment', observed=True)['retention'].agg(['mean', 'count'])
for idx, row in seg_stats.iterrows():
    print(f"{idx:10s} {row['mean']*100:5.1f}%  n={int(row['count'])}")

# Ad-hoc: Vehicles with best retention per price segment
print("\n=== BEST RETENTION BY PRICE RANGE ===")
# Cheap cars (<8万)
cheap = df[df['np_yuan'] < 80000].sort_values('retention', ascending=False)
print(f"\n--- Cheap Cars (<8万 new, top 10) ---")
for _, row in cheap.head(10).iterrows():
    print(f"{row['Title']:50s} Ret={row['retention']*100:5.1f}%  Price={row['Price']:5.2f}万  Age={row['age_years']:.2f}y")

# Mid-range (8-15万)
mid = df[(df['np_yuan'] >= 80000) & (df['np_yuan'] < 150000)].sort_values('retention', ascending=False)
print(f"\n--- Mid-range Cars (8-15万 new, top 10) ---")
for _, row in mid.head(10).iterrows():
    print(f"{row['Title']:50s} Ret={row['retention']*100:5.1f}%  Price={row['Price']:5.2f}万  Age={row['age_years']:.2f}y")

# Premium (15-30万)
prem = df[(df['np_yuan'] >= 150000) & (df['np_yuan'] < 300000)].sort_values('retention', ascending=False)
print(f"\n--- Premium Cars (15-30万 new, top 10) ---")
for _, row in prem.head(10).iterrows():
    print(f"{row['Title']:50s} Ret={row['retention']*100:5.1f}%  Price={row['Price']:5.2f}万  Age={row['age_years']:.2f}y")

# Luxury (>30万)
lux = df[df['np_yuan'] >= 300000].sort_values('retention', ascending=False)
print(f"\n--- Luxury Cars (>=30万 new, top 10) ---")
for _, row in lux.head(10).iterrows():
    print(f"{row['Title']:50s} Ret={row['retention']*100:5.1f}%  Price={row['Price']:5.2f}万  Age={row['age_years']:.2f}y")

# Model base analysis with all counts
print("\n=== FULL MODEL BASE ANALYSIS ===")
base_full = df.groupby('model_base').agg(
    avg_retention=('retention', 'mean'),
    count=('retention', 'count'),
    avg_age=('age_years', 'mean'),
    avg_price_wan=('Price', 'mean'),
    avg_np=('np_yuan', 'mean')
).reset_index()
base_full['avg_retention_pct'] = base_full['avg_retention'] * 100
base_full = base_full.sort_values('avg_retention', ascending=False)

for _, row in base_full.iterrows():
    print(f"{row['model_base']:35s} {row['avg_retention_pct']:5.1f}%  n={int(row['count']):2d}  age={row['avg_age']:.2f}y  price={row['avg_price_wan']:6.2f}万  new_price={row['avg_np']:>8.0f}元")
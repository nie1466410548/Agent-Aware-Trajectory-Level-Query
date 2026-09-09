import pandas as pd
import numpy as np

rows = db.query("""
  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Mileage", "Registration Date", "Posting Date", "Number of Previous Owners"
  FROM autohome
""")
df = db.frame(rows)

def parse_price(s):
    if pd.isna(s): return None
    s = str(s).replace(',', '').replace(' yuan', '').replace(' (variant)', '').replace(' (no space)', '').replace(' (with space)', '').replace(' yuan ', '').strip()
    try: return float(s)
    except: return None

df['np_yuan'] = df['np_raw'].apply(parse_price)
df['retention'] = df['Price'] * 10000 / df['np_yuan']

# New car price distribution
print("=== New car price distribution ===")
print(df['np_yuan'].describe())
print("\nPrice quantiles:")
print(df['np_yuan'].quantile([0.1, 0.25, 0.5, 0.75, 0.9]))

# Models with new price > 300k
premium_titles = df[df['np_yuan'] >= 300000]
print(f"\nRows with new car price >= 300k: {len(premium_titles)}")
for _, row in premium_titles.iterrows():
    print(f"  {row['Title']:55s} Price={row['Price']:7.2f}万  New={row['np_yuan']:>8.0f}  Class={row['Vehicle Class']}")

# Known expensive model names that appear with low prices
expensive_keywords = ['Mercedes', 'BMW iX', 'Cadillac', 'Zeekr', 'Gaohe', 'Li Xiang', 'Weilai', 'ET7', 'ES6', 'Xpeng G9', 'HiPhi', 'Model Y', 'Tang', 'Han EV', 'Deep Blue', 'Avita', 'LYRIQ', 'Volvo', 'Porsche', 'Audi', 'Polestar', 'IM L7', 'Lantu', 'Dengshi', 'D9']
suspect = df[df['Title'].str.contains('|'.join(expensive_keywords), case=False, na=False) & (df['np_yuan'] < 150000)]
print(f"\nSuspicious rows (expensive brand title but new price < 15万): {len(suspect)}")
for _, row in suspect.iterrows():
    print(f"  {row['Title']:55s} Price={row['Price']:5.2f}万  New={row['np_yuan']:>7.0f}  Class={row['Vehicle Class']}")

# How many rows total are the typical mini EV (new price 60k-90k)?
mini = df[(df['np_yuan'] >= 60000) & (df['np_yuan'] <= 100000)]
print(f"\nRows with new price 60k-100k (typical mini EV): {len(mini)} of {len(df)}")
print(f"Share: {len(mini)/len(df)*100:.1f}%")

# Check which vehicle classes dominate
print("\n=== Vehicle Class counts ===")
print(df['Vehicle Class'].value_counts())
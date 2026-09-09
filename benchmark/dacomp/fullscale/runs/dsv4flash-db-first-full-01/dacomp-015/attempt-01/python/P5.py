import pandas as pd
import numpy as np
import re

df = pd.read_csv('/work/parsed_data.csv')

# Parse Price (mixed formats: "2.25 million Yuan", "6780000 CNY", "5,800,000 Yuan", "1.85 million", etc.)
def parse_price(p):
    if pd.isna(p):
        return np.nan
    s = str(p).strip().lower()
    # Handle "million"
    m = re.search(r'([\d\.,]+)\s*million', s)
    if m:
        val = float(m.group(1).replace(',', ''))
        return val * 1_000_000
    # Handle plain numbers like "6780000", "5,800,000"
    m = re.search(r'([\d,]+)', s.replace(',', ''))
    if m:
        return float(m.group(1))
    return np.nan

df['price_num'] = df['Price'].apply(parse_price)

# Parse Area ("91.93 square meters", "129.49 sqm", "128.71 m²", etc.)
def parse_area(a):
    if pd.isna(a):
        return np.nan
    s = str(a).strip().lower()
    m = re.search(r'([\d\.,]+)', s)
    if m:
        return float(m.group(1).replace(',', ''))
    return np.nan

df['area_num'] = df['Area'].apply(parse_area)

print(f"Price parsed: {df['price_num'].notna().sum()} / {len(df)}")
print(f"Area parsed: {df['area_num'].notna().sum()} / {len(df)}")
print(df[['Price','price_num']].dropna().head(5).to_string())
print(df[['Area','area_num']].dropna().head(5).to_string())
print(df['price_num'].describe())
print(df['area_num'].describe())

# Price per sqm
df['price_sqm_num'] = df['Price/sqm'].apply(parse_price)
print(df['price_sqm_num'].describe())

df.to_csv('/work/parsed_data.csv', index=False)
print("saved")
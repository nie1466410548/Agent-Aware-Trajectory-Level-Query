import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

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

# Parse posting date (trim)
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

print(f"Total rows: {len(df)}")
print(f"Rows with valid retention: {df['retention'].notna().sum()}")
print(f"Avg retention: {df['retention'].mean():.2%}")
print(f"Min retention: {df['retention'].min():.2%}")
print(f"Max retention: {df['retention'].max():.2%}")

# Save cleaned data
df.to_parquet('/work/cleaned_data.parquet')

# Basic stats
print("\n--- Retention by Fuel Type ---")
print(df.groupby('Fuel Type')['retention'].describe())

print("\n--- Retention by Vehicle Class (top 10) ---")
print(df.groupby('Vehicle Class')['retention'].agg(['mean', 'count', 'std']).sort_values('mean', ascending=False))

print("\n--- Retention by Drivetrain ---")
print(df.groupby('Drivetrain_clean')['retention'].agg(['mean', 'count']).sort_values('mean', ascending=False))

print("\n--- Retention by Transmission ---")
print(df.groupby('Transmission_clean')['retention'].agg(['mean', 'count']).sort_values('mean', ascending=False))
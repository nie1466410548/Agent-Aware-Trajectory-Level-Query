import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load all data
df = db.frame(db.query("SELECT * FROM data"))

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nWatch Count stats:\n{df['Watch Count'].describe()}")
print(f"\nShowings stats:\n{df['Showings'].describe()}")

# Parse Floor Plan
def parse_floor_plan(fp):
    if pd.isna(fp):
        return (None, None)
    fp = fp.lower()
    # Extract bedroom count
    bed_match = re.search(r'(\d+)\s*bedroom', fp)
    # Extract living room count
    living_match = re.search(r'(\d+)\s*living\s*room', fp)
    bed = int(bed_match.group(1)) if bed_match else None
    living = int(living_match.group(1)) if living_match else None
    return (bed, living)

df[['bedrooms', 'living_rooms']] = df['Floor Plan'].apply(lambda x: pd.Series(parse_floor_plan(x)))

# Parse Floor into numeric level
def parse_floor(floor):
    if pd.isna(floor):
        return None, 'unknown'
    floor = str(floor).strip().lower()
    
    # Match "Nth floor", "Nst floor", "Nnd floor", "Nrd floor"
    m = re.search(r'^(\d+)(?:st|nd|rd|th)\s*floor$', floor)
    if m:
        return int(m.group(1)), 'specific'
    
    # Match "Floor N"
    m = re.search(r'^floor\s+(\d+)$', floor)
    if m:
        return int(m.group(1)), 'specific'
    
    # Match "N-story building" or "N floors"
    m = re.search(r'^(\d+)\s*(?:story\s*building|floors?)$', floor)
    if m:
        return int(m.group(1)), 'building_total'
    
    return None, 'other'

df[['floor_num', 'floor_type']] = df['Floor'].apply(lambda x: pd.Series(parse_floor(x)))

# Check if '40th Floor' etc. was parsed
print("\nUnique floor values:")
print(df[['Floor', 'floor_num', 'floor_type']].drop_duplicates().sort_values('floor_num').to_string())

# Categorize floor level
def categorize_floor(row):
    if row['floor_type'] != 'specific':
        return row['floor_type']
    n = row['floor_num']
    if n <= 6:
        return 'low_floor'
    elif n <= 18:
        return 'mid_floor'
    else:
        return 'high_floor'

df['floor_category'] = df.apply(categorize_floor, axis=1)

print("\nFloor category counts:")
print(df['floor_category'].value_counts())

# Categorize bedrooms
print("\nBedroom counts:")
print(df['bedrooms'].value_counts().sort_index())

# Categorize living rooms
print("\nLiving room counts:")
print(df['living_rooms'].value_counts().sort_index())

# Save parsed data
df.to_parquet('/work/parsed_data.parquet')
print("\nData saved.")
import pandas as pd
import numpy as np
import re

df = db.frame(db.query("SELECT * FROM data"))

# Parse Floor Plan
def parse_floor_plan(fp):
    if pd.isna(fp):
        return (None, None)
    fp = fp.lower()
    bed_match = re.search(r'(\d+)\s*bedroom', fp)
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
    m = re.search(r'^(\d+)(?:st|nd|rd|th)\s*floor$', floor)
    if m:
        return int(m.group(1)), 'specific'
    m = re.search(r'^floor\s+(\d+)$', floor)
    if m:
        return int(m.group(1)), 'specific'
    m = re.search(r'^(\d+)\s*(?:-?\s*story\s*building|floors?)$', floor)
    if m:
        return int(m.group(1)), 'building_total'
    return None, 'other'

df[['floor_num', 'floor_type']] = df['Floor'].apply(lambda x: pd.Series(parse_floor(x)))

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

df.to_csv('/work/parsed_data.csv', index=False)
print("\nSaved to /work/parsed_data.csv")
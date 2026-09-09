import pandas as pd
import numpy as np
import json
from collections import Counter

# Load all data
rows = db.query("SELECT * FROM sheet1 WHERE Views >= 5000000 ORDER BY Views DESC")
df = db.frame(rows)

# Get top viral videos (5M+ views)
viral_df = df[df['Views'] >= 5000000].copy()
print(f"Number of viral videos (5M+ views): {len(viral_df)}")
print(f"Number of viral videos (2M+ views): {len(df[df['Views'] >= 2000000])}")

# Let's look at the tags for viral videos
def extract_tags(tag_str):
    if pd.isna(tag_str) or tag_str.strip() == '':
        return []
    # Tags are comma-separated, sometimes with spaces
    tags = [t.strip().strip(',') for t in tag_str.split(',')]
    tags = [t for t in tags if t and t.strip() and t.strip() != ',']
    return tags

# Top 20 viral videos
print("\n=== Top 20 Viral Videos Info ===")
for _, row in viral_df.head(20).iterrows():
    tags = extract_tags(row['Video Tags'])
    print(f"Views: {row['Views']:>8}, Category: {str(row['Video Category']):>20}, Tags: {', '.join(tags[:5])}")

# Count tag frequencies in viral videos
all_tags = []
for _, row in viral_df.iterrows():
    tags = extract_tags(row['Video Tags'])
    all_tags.extend(tags)

tag_counter = Counter(all_tags)
print("\n=== Top 20 Tags in Viral Videos (5M+ views) ===")
for tag, count in tag_counter.most_common(20):
    print(f"  {tag}: {count}")
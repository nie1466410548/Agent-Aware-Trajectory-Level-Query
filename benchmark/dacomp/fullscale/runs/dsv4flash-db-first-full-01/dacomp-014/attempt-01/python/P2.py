import pandas as pd

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Check duplicates by title+creator
df['key'] = df['Title'] + '|' + df['Creator']
dup_counts = df.groupby('key').size().sort_values(ascending=False)
print("Top duplicate title+creator combos:")
print(dup_counts.head(15))

# How many unique videos vs rows
print(f"\nTotal rows: {len(df)}, unique title+creator: {df['key'].nunique()}")
print(f"Max duplicates for a video: {dup_counts.max()}")

# Distribution of duplicates
print("\nDuplicate count distribution:")
print(dup_counts.value_counts().sort_index())

# For duplicated videos, do views differ? (they're probably snapshots over months)
sample = df[df['key'] == dup_counts.index[0]]
print("\nSample duplicates:")
print(sample[['Title','Creator','Views','Overall Score','_id']].head(10))
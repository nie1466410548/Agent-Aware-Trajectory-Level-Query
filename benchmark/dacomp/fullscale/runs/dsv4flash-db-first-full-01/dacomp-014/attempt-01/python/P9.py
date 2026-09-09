import pandas as pd
import numpy as np
from collections import Counter

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)
df['key'] = df['Title'] + '|' + df['Creator']
df_u = df.drop_duplicates(subset='key').copy()

def extract_tags(tag_str):
    if pd.isna(tag_str) or str(tag_str).strip() == '':
        return []
    tags = [t.strip().strip(',') for t in str(tag_str).split(',')]
    tags = [t for t in tags if t and len(t) > 1 and t not in ('', ' ')]
    return tags

# Tags in top-ranked (Rank<=10) videos
top10 = df_u[df_u['Rank'] <= 10]
all_tags_top = []
for _, row in top10.iterrows():
    all_tags_top.extend(extract_tags(row['Video Tags']))
print("=== Top 25 Tags in Rank<=10 Videos ===")
for tag, count in Counter(all_tags_top).most_common(25):
    print(f"  {tag}: {count}")

# Compare to tags in low-ranked (Rank>80) videos
low = df_u[df_u['Rank'] >= 80]
all_tags_low = []
for _, row in low.iterrows():
    all_tags_low.extend(extract_tags(row['Video Tags']))
print("\n=== Top 25 Tags in Rank>=80 Videos ===")
for tag, count in Counter(all_tags_low).most_common(25):
    print(f"  {tag}: {count}")

# What fraction of top10 videos carry 'Guichu' or 'funny' tags
def has_tag(row, tag_keyword):
    tags = extract_tags(row['Video Tags'])
    return any(tag_keyword.lower() in t.lower() for t in tags)

for kw in ['Guichu', 'funny', 'dance', 'fitness', 'music', 'rap', 'MAD', 'Houlang', 'game', 'food']:
    pct_top = top10['key'].apply(lambda k: has_tag(top10.loc[top10['key']==k].iloc[0], kw)).mean()*100 if len(top10) else 0
    # simpler
    top_hit = top10.apply(lambda r: has_tag(r, kw), axis=1).mean()*100
    low_hit = low.apply(lambda r: has_tag(r, kw), axis=1).mean()*100
    print(f"  {kw}: top10={top_hit:.1f}% vs rank>=80={low_hit:.1f}%")
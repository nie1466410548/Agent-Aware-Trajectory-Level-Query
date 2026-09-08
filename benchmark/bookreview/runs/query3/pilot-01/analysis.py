import json
import pandas as pd

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/runs/query3/pilot-01/results/2669b1e746ef4ed59344d225827c9eb0.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/runs/query3/pilot-01/results/c2350423d5ae45fe916453ad50ec3f9e.json"))

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Check ID alignment
print("books:", len(bdf), "reviews:", len(rdf))
print("sample book_id:", bdf['book_id'].head(3).tolist())
print("sample purchase_id:", rdf['purchase_id'].head(3).tolist())

# Map purchaseid_N -> bookid_N
rdf['book_id'] = rdf['purchase_id'].str.replace('purchaseid_', 'bookid_', regex=False)

merged = rdf.merge(bdf[['book_id', 'title']], on='book_id', how='inner')
print("matched reviews:", len(merged), "of", len(rdf))

# ensure review_time >= 2020 (already filtered, double-check)
merged['review_time'] = pd.to_datetime(merged['review_time'])
merged = merged[merged['review_time'] >= '2020-01-01']

stats = merged.groupby(['book_id', 'title']).agg(
    avg_rating=('rating', 'mean'),
    n_reviews=('rating', 'count')
).reset_index().sort_values('avg_rating', ascending=False)

result = stats[stats['avg_rating'] >= 4.5]
print(result.to_string(index=False))
print("\nAll children's books with 2020+ reviews:")
print(stats.to_string(index=False))

with open('final_data.json', 'w') as f:
    json.dump(result.to_dict('records'), f, indent=2)

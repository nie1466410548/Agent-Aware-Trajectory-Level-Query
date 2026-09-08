import json
import pandas as pd

sales_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/music_brainz_20k/query3/full-01/results/dd8f3354db5d4de5adca29b3abf3edae.json"
tracks_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/music_brainz_20k/query3/full-01/results/2fb41827f1cf48abab195ac8beb47884.json"

sales = pd.DataFrame(json.load(open(sales_path)))
tracks = pd.DataFrame(json.load(open(tracks_path)))

print("sales rows:", len(sales), "tracks rows:", len(tracks))

df = sales.merge(tracks, on="track_id", how="left")

# 1) Top by individual track record (track_id)
top_track = df.sort_values("total_revenue_usd", ascending=False).head(10)
print("\nTOP 10 BY TRACK_ID:")
print(top_track.to_string(index=False))

# 2) Check duplicates: same normalized title+artist across multiple track_ids
def norm(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).strip().lower().split())

df["nkey"] = df["title"].map(norm) + "||" + df["artist"].map(norm)
dup = df.groupby("nkey").size()
print("\nNumber of title+artist keys with >1 track record:", (dup > 1).sum())

# 3) Aggregate by song (title+artist) across all duplicate records
song = df.groupby("nkey").agg(
    total_revenue_usd=("total_revenue_usd", "sum"),
    total_units=("total_units", "sum"),
    n_records=("track_id", "count"),
    title=("title", "first"),
    artist=("artist", "first"),
).sort_values("total_revenue_usd", ascending=False)
print("\nTOP 10 BY SONG (title+artist, duplicates combined):")
print(song.head(10).to_string(index=False))

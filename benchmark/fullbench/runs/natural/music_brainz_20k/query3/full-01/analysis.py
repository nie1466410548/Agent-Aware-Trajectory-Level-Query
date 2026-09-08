import json
import pandas as pd

sales = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/b77bf2b2ae1b49949a8f9249756cb310.json")
tracks = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/cfa169fd752543e28e3633f4755e2a0b.json")

df = sales.merge(tracks, on="track_id", how="left")
print("sales tracks:", len(sales), "tracks rows:", len(tracks), "merged:", len(df))
print("sales track_ids not in tracks:", df["title"].isna().sum())

# Top per track_id
top_id = df.sort_values("total_revenue", ascending=False).head(5)
print("\nTop by track_id:")
print(top_id[["track_id","title","artist","album","total_revenue"]].to_string(index=False))

# Normalize title/artist for song-level aggregation across duplicate sources
def norm(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).strip().lower().split())

df["norm_title"] = df["title"].map(norm)
df["norm_artist"] = df["artist"].map(norm)

# By title+artist
by_song = df.groupby(["norm_title","norm_artist"], as_index=False).agg(
    total_revenue=("total_revenue","sum"),
    n_track_ids=("track_id","nunique"),
    example_title=("title","first"),
    example_artist=("artist","first"),
)
by_song = by_song.sort_values("total_revenue", ascending=False)
print("\nTop by normalized title+artist:")
print(by_song.head(10).to_string(index=False))

# By title only
by_title = df.groupby("norm_title", as_index=False).agg(
    total_revenue=("total_revenue","sum"),
    n_track_ids=("track_id","nunique"),
    example_title=("title","first"),
)
by_title = by_title.sort_values("total_revenue", ascending=False)
print("\nTop by normalized title only:")
print(by_title.head(10).to_string(index=False))

# Do any duplicate groups (multiple track_ids same song) matter near the top?
multi = by_song[by_song.n_track_ids > 1]
print("\nSongs with multiple track_ids:", len(multi))

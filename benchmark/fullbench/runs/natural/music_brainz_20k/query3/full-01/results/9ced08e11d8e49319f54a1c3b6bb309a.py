import json
import pandas as pd

sales = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/b77bf2b2ae1b49949a8f9249756cb310.json")
tracks = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/cfa169fd752543e28e3633f4755e2a0b.json")
df = sales.merge(tracks, on="track_id", how="inner")

def norm(s):
    if pd.isna(s):
        return ""
    return " ".join(str(s).strip().lower().split())

df["norm_title"] = df["title"].map(norm)
df["norm_artist"] = df["artist"].map(norm)

junk = {"", "[untitled]", "unknown", "n.a.", "unk.", "[silence]", "untitled", "none"}
placeholder = df["norm_title"].isin(junk) | df["norm_title"].str.match(r"^\d{3}-?\s*$") | df["norm_title"].str.match(r"^\d{3}-\s*$")
d = df[~placeholder]

by_song = d.groupby(["norm_title","norm_artist"], as_index=False).agg(
    total_revenue=("total_revenue","sum"),
    n_track_ids=("track_id","nunique"),
    track_ids=("track_id", lambda x: sorted(x)),
    example_title=("title","first"),
    example_artist=("artist","first"),
    albums=("album", lambda x: sorted(set(str(a) for a in x))),
).sort_values("total_revenue", ascending=False)

print("Top songs after excluding placeholder titles:")
print(by_song.head(15).to_string(index=False))

# Show details of top few duplicate groups
for _, row in by_song[by_song.n_track_ids>1].head(5).iterrows():
    sub = df[(df.norm_title==row.norm_title)&(df.norm_artist==row.norm_artist)]
    print("\n=== ", row.example_title, "|", row.example_artist, " | total:", round(row.total_revenue,2))
    print(sub[["track_id","title","artist","album","source_id","total_revenue"]].to_string(index=False))

# Count of distinct track_ids matched vs unmatched
print("\nUnmatched sales track_ids:", len(sales) - len(df))

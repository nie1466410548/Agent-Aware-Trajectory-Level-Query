import json, re, difflib
import pandas as pd

sales = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/b77bf2b2ae1b49949a8f9249756cb310.json")
tracks = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/cfa169fd752543e28e3633f4755e2a0b.json")
df = sales.merge(tracks, on="track_id", how="inner")

print("rows per source:")
print(df.groupby("source_id").size())

# search for groovey variants
print("\nTitles containing 'groovey':")
print(df[df.title.str.contains("groovey", case=False, na=False)][["track_id","title","artist","album","source_id","total_revenue"]].to_string(index=False))

def norm(s):
    if pd.isna(s): return ""
    return " ".join(str(s).strip().lower().split())

# canonicalize: strip leading track-number prefixes like "005-" or "007 - "
def canon_title(t):
    t = norm(t)
    t = re.sub(r"^\d{3}\s*[-–]\s*", "", t)
    t = re.sub(r"[^\w\s]", "", t)
    return " ".join(t.split())

df["canon"] = df["title"].map(canon_title)
df["nartist"] = df["artist"].map(norm)

# Fuzzy dedup within artist: compare canonical titles pairwise per artist
rows = df.to_dict("records")
from collections import defaultdict
by_artist = defaultdict(list)
for r in rows:
    by_artist[r["nartist"]].append(r)

parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb

pairs = 0
for art, recs in by_artist.items():
    if len(recs) < 2: continue
    titles = [r["canon"] for r in recs]
    for i in range(len(recs)):
        for j in range(i+1, len(recs)):
            a, b = titles[i], titles[j]
            if not a or not b: continue
            if abs(len(a)-len(b)) > max(2, 0.15*max(len(a),len(b))): continue
            if difflib.SequenceMatcher(None, a, b).ratio() >= 0.87:
                union(recs[i]["track_id"], recs[j]["track_id"])
                pairs += 1

groups = defaultdict(lambda: {"rev":0.0,"ids":[],"titles":set(),"artists":set()})
for r in rows:
    g = groups[find(r["track_id"])]
    g["rev"] += r["total_revenue"]
    g["ids"].append(r["track_id"])
    g["titles"].add(str(r["title"]))
    g["artists"].add(str(r["artist"]))

gl = sorted(groups.values(), key=lambda g: -g["rev"])
print("\nfuzzy pairs merged:", pairs, "total groups:", len(gl))
print("\nTop 12 groups (fuzzy title within artist):")
for g in gl[:12]:
    print(round(g["rev"],2), len(g["ids"]), sorted(g["titles"])[:4], "|", sorted(g["artists"])[:2])

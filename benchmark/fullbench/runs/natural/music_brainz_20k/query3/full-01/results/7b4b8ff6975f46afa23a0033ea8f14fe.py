import json, re, difflib
import pandas as pd
from collections import defaultdict

sales = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/b77bf2b2ae1b49949a8f9249756cb310.json")
tracks = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/cfa169fd752543e28e3633f4755e2a0b.json")
df = sales.merge(tracks, on="track_id", how="inner")

# inspect Fischerspooner / Emerge rows
m = df[df.title.str.contains("emerge", case=False, na=False)]
print("All rows with 'emerge' in title:")
print(m[["track_id","title","artist","album","source_id","total_revenue"]].to_string(index=False))

def norm(s):
    if pd.isna(s): return ""
    return " ".join(str(s).strip().lower().split())

def canon_title(t, artist):
    t = norm(t)
    a = norm(artist)
    # source 2 style: "Artist - Title" when artist null
    if not a and " - " in t:
        a2, t2 = t.split(" - ", 1)
        a, t = a2, t2
    # strip leading track number prefix "005-" etc
    t = re.sub(r"^\d{1,3}\s*[-–]\s*", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t, a

ct = df.apply(lambda r: canon_title(r["title"], r["artist"]), axis=1)
df["canon"] = [x[0] for x in ct]
df["nartist"] = [x[1] for x in ct]

rows = df.to_dict("records")
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

by_artist = defaultdict(list)
for r in rows:
    by_artist[r["nartist"]].append(r)

def sim(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

for art, recs in by_artist.items():
    if len(recs) < 2: continue
    for i in range(len(recs)):
        for j in range(i+1, len(recs)):
            a, b = recs[i]["canon"], recs[j]["canon"]
            if not a or not b: continue
            r = sim(a, b)
            # exact or strong fuzzy; also allow one title being prefix of the other (album-suffix style)
            ok = r >= 0.85
            if not ok and (b.startswith(a) or a.startswith(b)):
                shorter = min(len(a), len(b)); longer = max(len(a), len(b))
                if shorter >= 6 and shorter/longer >= 0.5:
                    ok = True
            if ok:
                union(recs[i]["track_id"], recs[j]["track_id"])

groups = defaultdict(lambda: {"rev":0.0,"ids":[],"titles":set(),"artists":set(),"sources":set()})
for r in rows:
    g = groups[find(r["track_id"])]
    g["rev"] += r["total_revenue"]
    g["ids"].append(r["track_id"])
    g["titles"].add(str(r["title"]))
    g["artists"].add(str(r["artist"]))
    g["sources"].add(r["source_id"])

gl = sorted(groups.values(), key=lambda g: -g["rev"])
print("\nTop 15 groups:")
for g in gl[:15]:
    print(round(g["rev"],2), "n=",len(g["ids"]), "srcs=",sorted(g["sources"]))
    for t in sorted(g["titles"]): print("   ", t, "|", sorted(g["artists"]))

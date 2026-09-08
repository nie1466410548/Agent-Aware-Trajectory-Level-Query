import json, re, difflib
import pandas as pd
from collections import defaultdict

sales = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/b77bf2b2ae1b49949a8f9249756cb310.json")
tracks = pd.read_json("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/music_brainz_20k/query3/full-01/results/cfa169fd752543e28e3633f4755e2a0b.json")
df = sales.merge(tracks, on="track_id", how="inner")

def norm(s):
    if pd.isna(s): return ""
    return " ".join(str(s).strip().lower().split())

def canon(t, artist):
    t = norm(t); a = norm(artist)
    if not a and " - " in t:
        a, t = t.split(" - ", 1)
    t = re.sub(r"^\d{1,3}\s*[-–]\s*", "", t)
    return re.sub(r"\s+"," ",t).strip(), a

ct = df.apply(lambda r: canon(r["title"], r["artist"]), axis=1)
df["canon"] = [x[0] for x in ct]; df["nartist"] = [x[1] for x in ct]

rows = df.to_dict("records")
parent = {}
def find(x):
    parent.setdefault(x,x)
    while parent[x]!=x:
        parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[ra]=rb

by_artist = defaultdict(list)
for r in rows: by_artist[r["nartist"]].append(r)
for art, recs in by_artist.items():
    if len(recs)<2: continue
    for i in range(len(recs)):
        for j in range(i+1,len(recs)):
            a,b = recs[i]["canon"], recs[j]["canon"]
            if not a or not b: continue
            ok = difflib.SequenceMatcher(None,a,b).ratio() >= 0.85
            if not ok and (b.startswith(a) or a.startswith(b)):
                s,l = min(len(a),len(b)), max(len(a),len(b))
                if s>=6 and s/l>=0.5: ok=True
            if ok: union(recs[i]["track_id"], recs[j]["track_id"])

groups = defaultdict(lambda: {"rev":0.0,"ids":[],"titles":set(),"artists":set(),"sources":set()})
for r in rows:
    g = groups[find(r["track_id"])]
    g["rev"]+=r["total_revenue"]; g["ids"].append(r["track_id"])
    g["titles"].add(str(r["title"])); g["artists"].add(str(r["artist"])); g["sources"].add(r["source_id"])
gl = sorted(groups.values(), key=lambda g:-g["rev"])

# cluster size distribution
from collections import Counter
print("cluster size distribution:", Counter(len(g["ids"]) for g in gl))

# Verify top-5 clusters: show ALL tracks by same artist with similarity to cluster title
for rank,g in enumerate(gl[:5],1):
    main = sorted(g["titles"])[0]
    art = [a for a in g["artists"] if a!="nan"][0]
    c = canon(main, art)[0]
    sub = df[df.nartist==norm(art)].copy()
    sub["sim"] = sub.canon.map(lambda x: difflib.SequenceMatcher(None,c,x).ratio())
    sub = sub.sort_values("sim", ascending=False)
    print(f"\n#{rank} {round(g['rev'],2)} | artist={art} | members={len(g['ids'])}")
    print(sub[["track_id","title","album","source_id","total_revenue","sim"]].head(12).to_string(index=False))

print("\nFINAL TOP 5:")
for g in gl[:5]:
    art = [a for a in g["artists"] if a!="nan"]
    print(round(g["rev"],2), "|", sorted(g["titles"])[0], "|", art, "| ids:", sorted(g["ids"]))

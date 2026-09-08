import json, re
from collections import Counter

REV = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/eb152856605544129147da66dcb425f3.json"
BIZ = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/aa4c2b6e07274a28adccbf9c1bfcf806.json"
reviews = json.load(open(REV)); biz = json.load(open(BIZ))
bizmap = {b["business_id"]: b["description"] for b in biz}

def split_candidates(desc):
    d = desc.replace("'", " ")
    return [p.strip(' .;') for p in re.split(r',|\band\b', d) if p.strip(' .;')]

cand = Counter()
for b in biz:
    for p in split_candidates(b["description"]): cand[p] += 1
vocab = {p for p,c in cand.items() if c>=2 and not re.fullmatch(r'[A-Z]{2}',p) and p[0].isupper()}
vlist = sorted(vocab, key=len, reverse=True)

def extract_cats(desc):
    found=[]; occ=[False]*len(desc); low=desc.lower()
    for cat in vlist:
        cl=cat.lower(); start=0
        while True:
            i=low.find(cl,start)
            if i==-1: break
            j=i+len(cl)
            if (i==0 or not low[i-1].isalnum()) and (j==len(low) or not low[j].isalnum()) and not any(occ[i:j]):
                found.append(cat)
                for k in range(i,j): occ[k]=True
            start=i+1
    return set(found)

def num(s): return re.search(r'(\d+)$', s).group(1)
rev_biz = Counter("businessid_"+num(r["business_ref"]) for r in reviews if r["yr"] and r["yr"]>=2016)
print("distinct businesses reviewed:", len(rev_biz))
for bid, n in rev_biz.most_common():
    d = bizmap[bid]
    print(f"\n{bid} ({n} reviews): {sorted(extract_cats(d))}")
    print("   desc:", d)

import pandas as pd, numpy as np, re, json

# Load the already-queried peer set (S18) and market salary column (S19)
def load_rows(path):
    rows=[]
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

peer = pd.DataFrame(load_rows('results/S18.rows.jsonl'))
sal = pd.DataFrame(load_rows('results/S19.rows.jsonl'))

def parse_range(s):
    if s is None or (isinstance(s,float) and np.isnan(s)):
        return None
    s=str(s)
    # find all comma-stripped numbers
    nums = [int(x.replace(',','')) for x in re.findall(r'[\d,]+', s)]
    if not nums:
        return None
    if len(nums)>=2:
        lo, hi = nums[0], nums[1]
    else:
        lo = hi = nums[0]
    return (lo, hi)

peer['sal_parsed'] = peer['Salary Range'].apply(parse_range)
sal['sal_parsed'] = sal['Salary Range'].apply(parse_range)

peer['sal_min'] = peer['sal_parsed'].apply(lambda x: x[0] if x else None)
peer['sal_max'] = peer['sal_parsed'].apply(lambda x: x[1] if x else None)
peer['sal_mid'] = peer.apply(lambda r: (r['sal_min']+r['sal_max'])/2 if r['sal_parsed'] else None, axis=1)

print("=== PEER SET (insurance positions) ===")
for _,r in peer.iterrows():
    print(f"{r['Job Title'][:60]:62s} | {r['Company Name'][:45]:47s} | {str(r['Salary Range'])[:45]:47s} | mid={r['sal_mid']}")

print("\n=== PEER SALARY STATS (midpoint of headline range) ===")
mids = peer['sal_mid'].dropna()
print(f"n with salary = {len(mids)}; median={mids.median():.0f}; mean={mids.mean():.0f}; min={mids.min():.0f}; max={mids.max():.0f}")
print(f"P25={mids.quantile(0.25):.0f}; P75={mids.quantile(0.75):.0f}")

print("\n=== MARKET-WIDE SALARY STATS (all 4119 salaries) ===")
mm = sal['sal_parsed'].dropna()
print(f"n parsed={len(mm)}")
mids_all = pd.Series([(a+b)/2 for a,b in mm])
print(f"median={mids_all.median():.0f}; mean={mids_all.mean():.0f}; P75={mids_all.quantile(0.75):.0f}; P90={mids_all.quantile(0.90):.0f}; P95={mids_all.quantile(0.95):.0f}; max={mids_all.max():.0f}")
print(f"share of market jobs with mid >= 30000: {(mids_all>=30000).mean()*100:.2f}%")
print(f"share with mid >= 40000: {(mids_all>=40000).mean()*100:.2f}%")

# Save parsed data for later
peer.to_json('work/peer_parsed.json', orient='records', force_ascii=False)
sal.to_json('work/sal_parsed.json', orient='records', force_ascii=False)
print("\nSaved work/peer_parsed.json and work/sal_parsed.json")
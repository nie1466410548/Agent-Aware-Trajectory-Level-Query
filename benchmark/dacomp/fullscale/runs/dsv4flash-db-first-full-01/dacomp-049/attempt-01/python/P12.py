import pandas as pd, numpy as np, json, re, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':9, 'figure.dpi':110})

# Market salary distribution from parsed column
with open('/results/S19.rows.jsonl') as f:
    sal = pd.DataFrame([json.loads(l) for l in f], columns=['Salary Range'])
def parse_range(s):
    if s is None or (isinstance(s,float) and np.isnan(s)) or (isinstance(s,str) and s.strip()==''):
        return None
    nums = [int(x.replace(',','')) for x in re.findall(r'[\d,]+', str(s))]
    if not nums: return None
    return (nums[0], nums[1]) if len(nums)>=2 else (nums[0], nums[0])
mids = sal['Salary Range'].apply(lambda s: (lambda p: (p[0]+p[1])/2 if p else np.nan)(parse_range(s))).dropna()

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.hist(mids, bins=60, color='#bdbdbd', edgecolor='white', lw=0.3)
ax.axvline(30000, color='#d73027', ls='--', lw=1.4, label='Target salary floor 30,000')
ax.axvline(50000, color='#d73027', ls=':', lw=1.4, label='Target salary cap 50,000')
ax.axvline(mids.median(), color='#2c7fb8', ls='-', lw=1.2, label=f'Market median {mids.median():.0f}')
p95 = mids.quantile(0.95)
ax.axvline(p95, color='#756bb1', ls='-.', lw=1.2, label=f'Market P95 {p95:.0f}')
ax.set_xlim(0, 55000)
ax.set_xlabel('Monthly salary midpoint (yuan)')
ax.set_ylabel('Number of Xiamen job postings')
ax.set_title('Xiamen market salary distribution (n=4,119 postings with salary) — target posting sits at ~99th percentile')
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('fig4_market_context.png')
plt.close()
print('fig4 done', os.path.getsize('fig4_market_context.png'))

# percentile rank of target mid (40,000)
pct = (mids < 40000).mean()*100
print(f"Share of market postings with midpoint < 40,000: {pct:.2f}%")
pct_lo = (mids < 30000).mean()*100
print(f"Share with midpoint < 30,000: {pct_lo:.2f}%")

# Peer requirement table for report
peer['Salary Range'].fillna('(not disclosed)', inplace=True)
print("\nPeer list for report:")
for _, r in peer.iterrows():
    print("-", str(r['Job Title'])[:70], "|", str(r['Company Name'])[:50], "|", r['Salary Range'], "| Edu:", r['Education Requirement'], "| Exp:", r['Work Experience Requirement'])
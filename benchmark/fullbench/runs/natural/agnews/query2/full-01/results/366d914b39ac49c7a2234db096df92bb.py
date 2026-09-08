import json

# Load Amy Jones's articles retrieved from articles_database
rows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query2/full-01/results/a65f87c00fe640a4a0b83eeee60e8edb.json'))
assert len(rows) == 111, len(rows)

# Manual AG News-style classification (World / Sports / Business / Sci-Tech)
# based on title+description. Sci/Tech includes space, science research,
# software/internet/telecom/wireless, and tech-industry stories.
sci_tech_ids = {
    192,    # GameBoy mini-games (gaming/gadgets)
    2844,   # Students win national science competition
    2987,   # Teenager wins science award (energy from waves)
    15473,  # Rebuilding science in Iraq (nuclear physicist)
    17491,  # Intel lowers Q3 revenue estimates (tech industry)
    22354,  # NASA Genesis space probe crash
    24495,  # Space shuttle repair costs
    25960,  # Microsoft settles with UK phone maker Sendo
    35882,  # EMC e-mail storage software for Exchange
    41616,  # TechBrief: Vodafone (mobile telecom)
    46531,  # Ex-astronaut on space tourism
    64102,  # Texas Instruments chip profits (tech industry)
    73025,  # FCC approves wireless merger (Cingular/AT&T Wireless)
    89666,  # Vote-fraud theories spread by blogs (internet)
    91822,  # AMCC chipmaker layoffs (tech industry)
    92992,  # Study on fear/crowd behavior (science research)
    105804, # HP virus-throttling software
    106908, # XM satellite radio on cell phones
    108586, # eBay 'Want It Now' feature (internet)
    109601, # Chinese firm buys IBM PC business (tech industry)
    112770, # PayPal and Apple iTunes link-up
    116698, # Sprint-Nextel mobile merger (wireless)
    119651, # Ocean oversight: research, fisheries, pollution (science/env)
    126655, # Internet-based satellite spy technology
}

all_ids = {r['article_id'] for r in rows}
assert sci_tech_ids <= all_ids

n_total = len(rows)
n_st = len(sci_tech_ids)
frac = n_st / n_total
print(f"Total articles by Amy Jones: {n_total}")
print(f"Sci/Tech articles: {n_st}")
print(f"Fraction Sci/Tech: {n_st}/{n_total} = {frac:.4f} (~{frac:.2%})")
print("Sci/Tech titles:")
for r in rows:
    if r['article_id'] in sci_tech_ids:
        print(" -", r['article_id'], r['title'])

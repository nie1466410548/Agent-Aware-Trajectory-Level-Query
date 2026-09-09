import hashlib, re

# Get more address ids
res2 = db.query("SELECT DISTINCT customer360_id FROM customer360__address")
addr_ids = [r[0] for r in db.rows(res2)]
print("total distinct addr ids:", len(addr_ids))
print("len sample:", {len(x) for x in addr_ids})
print("first few:", addr_ids[:5])
# Check charset
nonhex = [x for x in addr_ids if not re.fullmatch(r'[0-9a-f]+', x)]
print("non-hex count:", len(nonhex), nonhex[:3])

# Get all latest emails
res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1
""")
rows = db.rows(res)
print("num customer rows:", len(rows))

addr_set = set(addr_ids)

# Try more variants: hash of email+something, or hash with random salt impossible.
# Try checking if address ids can be matched to stripe_customer_id (cus_...) or zendesk id hashed differently
for r in rows[:50]:
    email = r[0]; lid = r[1]; sid = r[2]; zid = r[3]; org = r[4]
    vals = [email, str(lid), sid or '', str(zid) if zid is not None else '', org or '']
    for label, val in zip(['email','lid','sid','zid','org'], vals):
        for algo in [hashlib.md5, hashlib.sha1]:
            for enc in [val.encode(), val.lower().encode(), val.strip().encode()]:
                h = algo(enc).hexdigest()
                if h in addr_set:
                    print("MATCH", label, val, h, algo.__name__)

# Also try treating customer360_id as sha of email @ domain
print("No direct match in first 50 samples likely")

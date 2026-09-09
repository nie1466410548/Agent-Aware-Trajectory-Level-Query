import hashlib

# Pull sample emails and ids from activity table
res = db.query("""
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM customer360__customer_activity_metrics
  WHERE rn = 1
""") if False else None

# Actually use the latest-record CTE to get clean samples
res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1 LIMIT 20
""")
rows = db.rows(res)
print(len(rows))
for r in rows[:5]:
    print(r)

# Pull some address ids
res2 = db.query("SELECT DISTINCT customer360_id, source_system FROM customer360__address LIMIT 20")
rows2 = db.rows(res2)
print(rows2[:5])

# Test hashing: md5 of email
candidates = set()
for r in rows:
    email = r['primary_email']
    lid = str(r['marketo_lead_id'])
    sid = r['stripe_customer_id'] or ''
    zid = str(r['zendesk_user_id'])
    for label, val in [('email', email), ('lid', lid), ('sid', sid), ('zid', zid)]:
        candidates.add((label, val, hashlib.md5(val.encode()).hexdigest()))
        candidates.add((label, val, hashlib.sha1(val.encode()).hexdigest()))
        candidates.add((label, val, hashlib.md5(val.lower().encode()).hexdigest()))

addr_ids = {r['customer360_id'] for r in rows2}
matches = [c for c in candidates if c[2] in addr_ids]
print("matches:", matches[:10])

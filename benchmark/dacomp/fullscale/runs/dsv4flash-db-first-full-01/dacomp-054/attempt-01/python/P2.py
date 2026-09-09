import hashlib

res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1 LIMIT 50
""")
rows = db.rows(res)
print("row type:", type(rows), len(rows))
print("first:", rows[0])

res2 = db.query("SELECT DISTINCT customer360_id, source_system FROM customer360__address LIMIT 200")
rows2 = db.rows(res2)
addr_ids = set()
for r in rows2:
    addr_ids.add(r[0])
print("addr sample:", rows2[0])

candidates = []
for r in rows:
    email = r[0] if isinstance(r, list) else r['primary_email']
    lid = r[1] if isinstance(r, list) else r['marketo_lead_id']
    sid = r[2] if isinstance(r, list) else r['stripe_customer_id']
    zid = r[3] if isinstance(r, list) else r['zendesk_user_id']
    vals = [('email', email), ('lid', str(lid)), ('sid', sid or ''), ('zid', str(zid))]
    for label, val in vals:
        for algo in [hashlib.md5, hashlib.sha1, hashlib.sha256]:
            candidates.append((label, val, algo(val.encode()).hexdigest(), algo.__name__))
            candidates.append((label, val, algo(val.lower().encode()).hexdigest(), algo.__name__+'_low'))

matches = [c for c in candidates if c[2] in addr_ids]
print("matches found:", len(matches))
for m in matches[:20]:
    print(m)

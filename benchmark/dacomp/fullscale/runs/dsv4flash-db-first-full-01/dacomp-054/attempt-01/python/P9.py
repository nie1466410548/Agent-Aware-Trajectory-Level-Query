import hashlib

resa = db.query("SELECT DISTINCT customer360_id, source_system FROM customer360__address")
addr_rows = db.rows(resa)
marketo_ids = {r[0] for r in addr_rows if r[1] == 'marketo'}
stripe_ids = {r[0] for r in addr_rows if r[1] == 'stripe'}

# Get all marketo_lead_ids (distinct) and stripe ids from the activity table (latest per email)
res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id FROM la WHERE rn=1
""")
rows = db.rows(res)

patterns = ['marketo_{}', 'marketo{}', 'lead_{}', 'lead{}', 'm{}', 'ml{}', '{}_marketo', 'cus_{}', 'stripe_{}', 'zd_{}', 'z{}', 'zendesk_{}']
match_counts = {p: 0 for p in patterns}

for r in rows:
    lid = r[1]; sid = r[2]; zid = r[3]
    candidates = {}
    if lid is not None:
        for p in patterns:
            candidates[f"{p.format(lid)}-market"] = hashlib.md5(p.format(lid).encode()).hexdigest()
    if sid:
        candidates[f"cus_{sid}"] = hashlib.md5(sid.encode()).hexdigest()
        candidates[f"stripe_{sid}"] = hashlib.md5(f"stripe_{sid}".encode()).hexdigest()
    for label, h in candidates.items():
        if h in marketo_ids or h in stripe_ids:
            print("MATCH:", label, h)
            break

# Also try: maybe customer360_id is a random UUID -> md5. Can't map.
# Try counting: are there 9671 marketo customer ids which is exactly number of (email, source) combos?
print("distinct marketo addr ids:", len(marketo_ids), "distinct stripe addr ids:", len(stripe_ids))
print("distinct customer emails:", len(rows))

# Check the distribution of addresses per customer360_id for marketo
res3 = db.query("""
  SELECT customer360_id, COUNT(*) cnt FROM customer360__address 
  WHERE source_system='marketo' GROUP BY customer360_id ORDER BY cnt DESC LIMIT 10
""")
print("marketo addr counts per id:", db.rows(res3)[:10])

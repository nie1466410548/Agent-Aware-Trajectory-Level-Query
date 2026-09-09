import hashlib

# Get all marketo_lead_id, stripe_customer_id, zendesk_user_id combos
res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1
""")
rows = db.rows(res)

# Get all address ids
resa = db.query("SELECT DISTINCT customer360_id, source_system FROM customer360__address")
addr_rows = db.rows(resa)
addr_marketo = {r[0] for r in addr_rows if r[1] == 'marketo'}
addr_stripe = {r[0] for r in addr_rows if r[1] == 'stripe'}
print("Market addresses:", len(addr_marketo), "Stripe addresses:", len(addr_stripe))

# Try hash of primary_email + primary_organization
for r in rows[:100]:
    email = r[0]; lid = r[1]; sid = r[2]; zid = r[3]; org = r[4]
    # Try concatenation with different separators
    for comb, label in [
        (f"{email}|{org}", "email|org"),
        (f"{email}|{lid}", "email|lid"),
        (f"{lid}|{email}", "lid|email"),
        (f"{email}:{org}", "email:org"),
        (f"{email}.{org}", "email.org"),
        (f"{lid}|{org}", "lid|org"),
        (f"{email}|{sid}", "email|sid"),
        (f"{sid}|{email}", "sid|email"),
    ]:
        h = hashlib.md5(comb.encode()).hexdigest()
        if h in addr_marketo:
            print(f"MATCH marketo: {label} -> {comb} -> {h}")
        if h in addr_stripe:
            print(f"MATCH stripe: {label} -> {comb} -> {h}")

print("No matches found in first 100 samples")
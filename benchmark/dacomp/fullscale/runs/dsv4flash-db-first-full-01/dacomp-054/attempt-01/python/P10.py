import hashlib

resa = db.query("SELECT DISTINCT customer360_id FROM customer360__address")
addr_ids = {r[0] for r in db.rows(resa)}

res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, primary_organization, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1
""")
rows = db.rows(res)

# Try hashing primary_organization
for r in rows:
    org = r[1]
    if org:
        for prefix in ['', 'org:', 'company:', 'account:']:
            h = hashlib.md5(f"{prefix}{org}".encode()).hexdigest()
            if h in addr_ids:
                print(f"MATCH org: {prefix}{org} -> {h}")

# Check if there are 9671 marketo customer360_ids, which might be 4734 * 2 (approx)
# Let me check if the marketo source addresses have a direct mapping to funnel records
# by checking if the number of distinct customer360_ids for marketo (9671) relates to 
# number of distinct funnel records
res_f = db.query("SELECT COUNT(DISTINCT marketo_lead_id || '-' || stripe_customer_id || '-' || zendesk_user_id) FROM customer360__conversion_funnel_analysis")
print("distinct funnel combos:", db.rows(res_f)[0][0])

# Check distinct funnel_analysis_timestamp + marketo_lead_id combos
res_f2 = db.query("SELECT COUNT(DISTINCT marketo_lead_id || '-' || funnel_analysis_timestamp) FROM customer360__conversion_funnel_analysis")
print("distinct lead+ts combos:", db.rows(res_f2)[0][0])

# Maybe the address table has a different number of customers altogether
# Let me check if there are countries in the address table
res_a = db.query("SELECT DISTINCT country FROM customer360__address ORDER BY country LIMIT 20")
print("countries sample:", [r[0] for r in db.rows(res_a)])

# Count distinct countries
res_a2 = db.query("SELECT COUNT(DISTINCT country) FROM customer360__address")
print("num countries:", db.rows(res_a2)[0][0])
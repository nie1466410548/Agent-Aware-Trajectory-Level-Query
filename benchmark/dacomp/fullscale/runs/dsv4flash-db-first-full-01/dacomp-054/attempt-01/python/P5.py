import hashlib

resa = db.query("SELECT DISTINCT customer360_id, source_system FROM customer360__address")
addr_rows = db.rows(resa)
addr_set = {r[0] for r in addr_rows}

res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1
""")
rows = db.rows(res)

# Build a dict of md5->candidate for common patterns across all customers (4734)
# Too many combos; test on the assumption that customer360_id = md5(email) or md5 of an id string formatted
# Check the frequency of md5(email) across all: how many emails' md5s are in addr_set
count = 0
for r in rows:
    email = r[0]
    if hashlib.md5(email.encode()).hexdigest() in addr_set:
        count += 1
print("md5(email) matches:", count)

count2 = 0
for r in rows:
    lid = str(r[1])
    if hashlib.md5(lid.encode()).hexdigest() in addr_set:
        count2 += 1
print("md5(lid str) matches:", count2)

# Check md5 of email domain
count3 = 0
for r in rows:
    dom = r[0].split('@')[1]
    if hashlib.md5(dom.encode()).hexdigest() in addr_set:
        count3 += 1
print("md5(domain) matches:", count3)

# Check whether marketo source addresses might be hashes of marketo_lead_id
count4 = 0
for r in rows:
    lid = str(r[1])
    if hashlib.md5(lid.encode()).hexdigest() in addr_set:
        count4 += 1
print("md5(lid) full set:", count4)

# Check md5 of stripe_customer_id
count5 = 0
for r in rows:
    sid = r[2]
    if sid and hashlib.md5(sid.encode()).hexdigest() in addr_set:
        count5 += 1
print("md5(sid) matches:", count5)

# zendesk user id
count6 = 0
for r in rows:
    zid = str(r[3]) if r[3] is not None else ''
    if zid and hashlib.md5(zid.encode()).hexdigest() in addr_set:
        count6 += 1
print("md5(zid) matches:", count6)

print("Sample addr ids:", sorted(addr_set)[:10])

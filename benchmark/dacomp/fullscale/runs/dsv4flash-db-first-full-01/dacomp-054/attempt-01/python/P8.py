import hashlib

# Get all emails and all address ids
resa = db.query("SELECT DISTINCT customer360_id FROM customer360__address")
addr_ids = {r[0] for r in db.rows(resa)}

res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email FROM la WHERE rn=1
""")
emails = [r[0] for r in db.rows(res)]

# Try various email transformations
for email in emails[:2000]:
    for transformed in [
        email.lower(),
        email.strip(),
        email.lower().strip(),
        email.replace('@', '.'),
        email.replace('@', ''),
        email.replace('.', ''),
        email.replace('@', '-at-'),
        email.upper(),
        email.replace('@', '+'),
        email.replace('@', '='),
        f"mailto:{email}",
        f"email:{email}",
        email.split('@')[0],
        f"{email.split('@')[0]}|{email.split('@')[1]}",
    ]:
        h = hashlib.md5(transformed.encode()).hexdigest()
        if h in addr_ids:
            print(f"MATCH! email={email}, transform={transformed}, hash={h}")
            break
else:
    print("No match in first 2000 emails")

# Also try md5 of email with UUID5 namespace
# Try sha256
for email in emails[:200]:
    h = hashlib.sha256(email.encode()).hexdigest()
    if h in addr_ids:
        print(f"sha256 match: {email}")
        
print("Done checking")
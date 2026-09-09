import hashlib

# Check if any column values in the customer tables are 32-hex ids
res = db.query("""
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT * FROM la WHERE rn=1 LIMIT 3
""")
rows = db.rows(res)
cols = db.query("SELECT * FROM customer360__customer_activity_metrics LIMIT 1")
col_names = [c['name'] for c in cols['executions'][0]['columns']] if False else list(db.query("SELECT * FROM customer360__customer_activity_metrics LIMIT 1")['executions'][0]['columns'])
print(col_names)

import re
hexpat = re.compile(r'^[0-9a-f]{32}$')
# scan text columns of the 3 tables for 32-hex values
for tbl in ['customer360__customer_activity_metrics', 'customer360__conversion_funnel_analysis', 'customer360__customer_value_analysis']:
    res = db.query(f"SELECT * FROM {tbl} LIMIT 1000")
    rows = db.rows(res)
    colnames = list(res['executions'][0]['columns'])
    found = {}
    for r in rows:
        for c in colnames:
            v = r[c]
            if isinstance(v, str) and hexpat.match(v):
                found.setdefault(c, set()).add(v)
    print(tbl, {k: len(v) for k, v in found.items() if len(v) > 0})

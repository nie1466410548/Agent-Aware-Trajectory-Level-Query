import re
hexpat = re.compile(r'^[0-9a-f]{32}$')

# Get column names from each table
for tbl in ['customer360__customer_activity_metrics', 'customer360__conversion_funnel_analysis', 'customer360__customer_value_analysis']:
    res = db.query(f"SELECT * FROM {tbl} LIMIT 1")
    colnames = res['executions'][0]['columns']
    res2 = db.query(f"SELECT * FROM {tbl} LIMIT 2000")
    rows = db.rows(res2)
    found = {}
    for r in rows:
        for i, c in enumerate(colnames):
            if isinstance(r[i], str) and hexpat.match(r[i]):
                found.setdefault(c, set()).add(r[i])
    print(tbl, {k: len(v) for k, v in found.items()})
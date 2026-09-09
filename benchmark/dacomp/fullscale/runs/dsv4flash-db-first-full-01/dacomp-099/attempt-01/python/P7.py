import pandas as pd

# Query conversation_enhanced only (no join)
sql1 = """
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type
FROM intercom__conversation_enhanced
WHERE all_contact_company_names = 'Edge Platforms'
"""
try:
    df1 = db.frame(db.query(sql1))
    print("No-join Edge Platforms rows:", df1.shape)
except Exception as e:
    print("Error no-join:", e)

# Query metrics alone
sql2 = """
SELECT conversation_id, count_total_parts
FROM intercom__conversation_metrics
LIMIT 100
"""
try:
    df2 = db.frame(db.query(sql2))
    print("Metrics sample:", df2.shape)
except Exception as e:
    print("Error metrics:", e)

# Check duplicate conversation ids
sql3 = "SELECT conversation_id, COUNT(*) as n FROM intercom__conversation_enhanced GROUP BY conversation_id HAVING n > 1 LIMIT 5"
res = db.query(sql3)
print("Duplicate conv ids in enhanced:", res['executions'][0]['row_count'])
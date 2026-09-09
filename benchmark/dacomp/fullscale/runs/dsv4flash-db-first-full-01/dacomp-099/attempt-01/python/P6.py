import pandas as pd
import numpy as np

# Try loading conversations for just one company to test completeness
sql = """
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type,
       count_total_parts
FROM intercom__conversation_enhanced c
LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
WHERE c.all_contact_company_names = 'Edge Platforms'
"""
try:
    df = db.frame(db.query(sql))
    print("Edge Platforms rows:", df.shape)
except Exception as e:
    print("Error:", e)

# Check overall result completeness behavior - query count only
res = db.query("SELECT COUNT(*) as n FROM intercom__conversation_enhanced")
print(res)
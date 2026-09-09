import pandas as pd
import numpy as np
from scipy import stats

# ============ SLA name distribution by type ============
result = db.query("""
SELECT ce.conversation_initiated_type, ce.sla_name, ce.sla_status, ce.conversation_rating, 
       ce.conversation_remark, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
""")
conv = db.frame(result)
print("="*70)
print("SLA NAME DISTRIBUTION BY TYPE")
print("="*70)
print(pd.crosstab(conv['conversation_initiated_type'], conv['sla_name'], normalize='index').round(3))
print()
print(pd.crosstab(conv['conversation_initiated_type'], conv['sla_name']))

# ============ Conversation rating remark (sentiment) ============
print("\n" + "="*70)
print("CONVERSATION RATING REMARK BY TYPE")
print("="*70)
print(pd.crosstab(conv['conversation_initiated_type'], conv['conversation_remark'], normalize='index').round(3))
print()
print(pd.crosstab(conv['conversation_initiated_type'], conv['conversation_remark']))

# ============ Company industry data ============
# Join contacts to companies
result2 = db.query("""
SELECT ce.all_conversation_contacts AS contact_id, 
       ce.conversation_initiated_type,
       c.industry,
       c.plan_name
FROM intercom__conversation_enhanced ce
LEFT JOIN intercom__contact_enhanced ct ON ce.all_conversation_contacts = ct.contact_id
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 10
""")
# Let me check the contact-company mapping more carefully
print("\n" + "="*70)
print("COMPANY DATA (sample)")
print("="*70)
result2 = db.query("""
SELECT DISTINCT ct.all_contact_company_names, c.company_id, c.industry, c.plan_name
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 20
""")
print(db.frame(result2).head(20))

# Check how many contacts can be matched to companies
result3 = db.query("""
SELECT COUNT(*) as total,
       SUM(CASE WHEN c.company_id IS NOT NULL THEN 1 ELSE 0 END) as matched
FROM (
  SELECT DISTINCT all_contact_company_names as company_name
  FROM intercom__contact_enhanced
) ct
LEFT JOIN intercom__company_enhanced c ON ct.company_name = c.company_name
""")
print(db.frame(result3))
SELECT c.account_id, c.department, c.title
FROM salesforce__contact_enhanced c
WHERE c.account_id IN (
  SELECT a.account_id FROM salesforce__customer_360_view a WHERE a.annual_revenue >= 71234915
)
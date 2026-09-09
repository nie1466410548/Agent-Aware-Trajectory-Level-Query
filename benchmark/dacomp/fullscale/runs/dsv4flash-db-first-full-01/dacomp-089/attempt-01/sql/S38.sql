SELECT c.title, COUNT(*) AS cnt FROM salesforce__contact_enhanced c
WHERE c.account_id IN (
  SELECT a.account_id FROM salesforce__customer_360_view a WHERE a.annual_revenue >= 71234915
)
GROUP BY c.title HAVING cnt > 5 ORDER BY cnt DESC LIMIT 40
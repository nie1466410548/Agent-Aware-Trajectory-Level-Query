SELECT owner_id, account_owner_name, COUNT(*) AS num_customers, 
  SUM(annual_revenue) AS total_revenue,
  ROUND(AVG(annual_revenue), 2) AS avg_revenue,
  SUM(total_contacts) AS total_contacts,
  SUM(total_opportunities) AS total_opps
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY num_customers DESC
LIMIT 20
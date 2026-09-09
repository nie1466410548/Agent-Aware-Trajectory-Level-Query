SELECT owner_id, COUNT(*) AS num_customers,
  SUM(annual_revenue) AS total_annual_revenue,
  SUM(total_contacts) AS total_contacts,
  SUM(total_opportunities) AS total_opps,
  SUM(won_opportunities) AS won_opps,
  ROUND(AVG(annual_revenue), 2) AS avg_revenue
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY num_customers DESC
LIMIT 10
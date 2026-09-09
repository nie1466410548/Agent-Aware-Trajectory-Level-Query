SELECT 
  COUNT(*) AS total_accounts,
  COUNT(annual_revenue) AS with_rev,
  MIN(annual_revenue) AS min_rev,
  MAX(annual_revenue) AS max_rev,
  AVG(annual_revenue) AS avg_rev,
  SUM(CASE WHEN number_of_employees IS NULL THEN 1 ELSE 0 END) AS null_emp,
  SUM(CASE WHEN total_contacts IS NULL THEN 1 ELSE 0 END) AS null_tc
FROM salesforce__customer_360_view
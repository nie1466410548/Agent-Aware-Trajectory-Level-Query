SELECT COUNT(*) AS cnt, MIN(annual_revenue) AS min_rev, MAX(annual_revenue) AS max_rev, AVG(annual_revenue) AS avg_rev, SUM(annual_revenue) AS total_rev
FROM (
  SELECT annual_revenue FROM salesforce__customer_360_view 
  WHERE annual_revenue IS NOT NULL 
  ORDER BY annual_revenue DESC 
  LIMIT 2000
)
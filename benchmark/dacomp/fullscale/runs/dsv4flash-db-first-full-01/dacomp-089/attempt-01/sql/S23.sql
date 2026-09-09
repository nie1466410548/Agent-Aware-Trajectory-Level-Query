SELECT percentile, MIN(rev) AS rev_threshold FROM (
  SELECT annual_revenue AS rev, NTILE(20) OVER (ORDER BY annual_revenue DESC) AS percentile
  FROM salesforce__customer_360_view WHERE annual_revenue IS NOT NULL
) GROUP BY percentile
SELECT annual_revenue FROM salesforce__customer_360_view 
WHERE annual_revenue IS NOT NULL 
ORDER BY annual_revenue DESC 
LIMIT 1 OFFSET 1999
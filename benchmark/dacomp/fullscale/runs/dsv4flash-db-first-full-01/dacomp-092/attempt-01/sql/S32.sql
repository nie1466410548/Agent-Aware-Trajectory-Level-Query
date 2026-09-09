SELECT DISTINCT revenue_year, revenue_quarter, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
GROUP BY revenue_year, revenue_quarter
ORDER BY revenue_year, revenue_quarter
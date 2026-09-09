SELECT fiscal_year, COUNT(*) AS n, SUM(is_won) AS won
FROM salesforce__opportunity_enhanced
GROUP BY fiscal_year ORDER BY fiscal_year
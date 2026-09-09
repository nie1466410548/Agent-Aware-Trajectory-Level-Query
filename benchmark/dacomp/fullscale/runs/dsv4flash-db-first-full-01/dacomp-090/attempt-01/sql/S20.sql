SELECT dashboard_month, collection_rate_percentage,
  collection_rate_percentage - LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS mom_change
FROM quickbooks__financial_dashboard
ORDER BY dashboard_month DESC
LIMIT 13
SELECT dashboard_month, collection_rate_percentage,
  collection_rate_percentage - LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS mom_change,
  CASE WHEN collection_rate_percentage < LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) THEN 1 ELSE 0 END AS is_decline
FROM quickbooks__financial_dashboard
WHERE dashboard_month >= '2024-10-01'
ORDER BY dashboard_month
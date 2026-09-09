
SELECT package_name,
       SUM(daily_net_revenue) AS rev2024,
       SUM(store_visitors) AS vis2024,
       SUM(store_acquisitions) AS acq2024,
       SUM(daily_net_revenue)/NULLIF(SUM(store_acquisitions),0) AS rev_per_acq,
       SUM(store_acquisitions)*1.0/NULLIF(SUM(store_visitors),0) AS conv_rate
FROM google_play__comprehensive_performance_dashboard
WHERE date_day >= '2024-01-01' AND date_day < '2025-01-01'
GROUP BY package_name
ORDER BY package_name

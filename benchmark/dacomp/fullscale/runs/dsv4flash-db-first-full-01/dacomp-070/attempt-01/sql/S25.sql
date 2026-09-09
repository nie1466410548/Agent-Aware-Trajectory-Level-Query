
SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       SUM(cr.store_listing_visitors) AS visitors,
       SUM(cr.store_listing_acquisitions) AS acquisitions,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad, AVG(ts.active_devices) AS active_devices,
       AVG(ts.daily_churn_rate) AS churn
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name

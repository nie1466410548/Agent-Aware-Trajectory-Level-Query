
SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name
HAVING SUM(cr.store_listing_visitors) > 0
ORDER BY cr.date_day, cr.region, cr.package_name

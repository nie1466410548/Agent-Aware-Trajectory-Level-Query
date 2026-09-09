SELECT 'campaign_report' AS tbl, COUNT(*) AS rows, COUNT(DISTINCT campaign_id) AS campaigns, COUNT(DISTINCT year_month) AS months, MIN(year_month) AS min_m, MAX(year_month) AS max_m FROM google_ads__campaign_report
UNION ALL
SELECT 'device_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_month), MIN(year_month), MAX(year_month) FROM google_ads__device_report
UNION ALL
SELECT 'geo_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_month), MIN(year_month), MAX(year_month) FROM google_ads__geo_report
UNION ALL
SELECT 'keyword_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_quarter), MIN(year_quarter), MAX(year_quarter) FROM google_ads__keyword_report
UNION ALL
SELECT 'campaigns', COUNT(*), COUNT(DISTINCT campaign_id), NULL, NULL, NULL FROM campaigns
UNION ALL
SELECT 'keywords', COUNT(*), COUNT(DISTINCT keyword_id), NULL, NULL, NULL FROM keywords
UNION ALL
SELECT 'ad_groups', COUNT(*), COUNT(DISTINCT ad_group_id), NULL, NULL, NULL FROM ad_groups
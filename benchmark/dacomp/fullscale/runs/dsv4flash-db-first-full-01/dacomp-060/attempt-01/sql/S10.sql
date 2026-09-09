WITH ag AS (
  SELECT ad_group_id, SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(conversions) AS conversions
  FROM google_ads__ad_group_report GROUP BY ad_group_id
)
SELECT 
  MIN(clicks) AS min_clicks, MAX(clicks) AS max_clicks,
  MIN(impressions) AS min_impr, MAX(impressions) AS max_impr,
  MIN(conversions) AS min_conv, MAX(conversions) AS max_conv
FROM ag
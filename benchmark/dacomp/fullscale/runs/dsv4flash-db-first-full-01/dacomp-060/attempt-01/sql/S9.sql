WITH ag AS (
  SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_id, account_name, status,
         SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
         SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
)
SELECT 
  COUNT(*) AS n_ag,
  SUM(CASE WHEN impressions>0 AND clicks>0 THEN 1 ELSE 0 END) AS n_usable,
  SUM(CASE WHEN impressions>0 THEN 1 ELSE 0 END) AS n_impr,
  SUM(CASE WHEN clicks>0 THEN 1 ELSE 0 END) AS n_clicks,
  SUM(CASE WHEN conversions>0 THEN 1 ELSE 0 END) AS n_conv
FROM ag
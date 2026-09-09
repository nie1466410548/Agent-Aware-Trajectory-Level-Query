WITH ag AS (
  SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_id, account_name, status,
         SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
         SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
)
SELECT ad_group_id, ad_group_name, campaign_name, account_name, status,
       impressions, clicks, spend, conversions, conv_value, vtc,
       ROUND(CAST(clicks AS REAL) / impressions, 6) AS ctr,
       ROUND(CAST(conversions AS REAL) / clicks, 6) AS cvr
FROM ag
ORDER BY ad_group_id
-- Per-ad-group aggregates with campaign_id
SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_name, status,
       SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
       SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc,
       ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) AS ctr,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS cvr
FROM google_ads__ad_group_report
GROUP BY ad_group_id
ORDER BY ad_group_id
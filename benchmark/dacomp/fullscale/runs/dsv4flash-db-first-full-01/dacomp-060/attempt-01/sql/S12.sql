-- Get campaign-level aggregates for expected CVR (per campaign)
SELECT campaign_id, campaign_name, account_name,
       SUM(impressions) AS campaign_impressions,
       SUM(clicks) AS campaign_clicks,
       SUM(spend) AS campaign_spend,
       SUM(conversions) AS campaign_conversions,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS campaign_cvr
FROM google_ads__ad_group_report
GROUP BY campaign_id
ORDER BY campaign_id
-- Campaign-level aggregates from campaign_report (aggregated per campaign)
SELECT campaign_id, campaign_name, account_name, advertising_channel_type, advertising_channel_subtype, status,
       SUM(impressions) AS campaign_impressions, SUM(clicks) AS campaign_clicks, SUM(spend) AS campaign_spend,
       SUM(conversions) AS campaign_conversions,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS campaign_cvr
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY campaign_id
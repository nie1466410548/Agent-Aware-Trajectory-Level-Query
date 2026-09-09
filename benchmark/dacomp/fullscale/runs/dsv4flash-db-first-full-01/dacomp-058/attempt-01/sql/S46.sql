
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost
FROM google_ads__device_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type

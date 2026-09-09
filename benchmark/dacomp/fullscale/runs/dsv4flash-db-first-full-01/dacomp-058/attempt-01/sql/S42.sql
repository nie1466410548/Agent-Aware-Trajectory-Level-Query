
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr
FROM google_ads__device_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type

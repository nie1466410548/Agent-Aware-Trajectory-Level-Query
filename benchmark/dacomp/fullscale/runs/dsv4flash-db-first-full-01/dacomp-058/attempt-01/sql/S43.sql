
SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr, ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, cost DESC

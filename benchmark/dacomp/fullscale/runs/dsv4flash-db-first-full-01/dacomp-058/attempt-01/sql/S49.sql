
SELECT 
  ROUND(SUM(CASE WHEN campaign_id IN (105,135,36,184,180,56,69,148,178,27) THEN cost ELSE 0 END),0) AS prob_cost,
  ROUND(SUM(cost),0) AS total_cost,
  ROUND(100.0 * SUM(CASE WHEN campaign_id IN (105,135,36,184,180,56,69,148,178,27) THEN cost ELSE 0 END)/SUM(cost), 1) AS pct
FROM google_ads__campaign_report

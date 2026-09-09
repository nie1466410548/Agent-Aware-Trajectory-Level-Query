SELECT
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS roas_lt_08,
  COUNT(CASE WHEN (conversion_value/NULLIF(cost,0)) < 0.8 THEN 1 END) AS cv_cost_lt_08,
  COUNT(CASE WHEN roas < 0.8 AND (conversion_value/NULLIF(cost,0)) >= 0.8 THEN 1 END) AS mismatch,
  ROUND(AVG(ABS(roas - conversion_value/NULLIF(cost,0))),4) AS avg_abs_diff,
  ROUND(CORR(roas, conversion_value/NULLIF(cost,0)),4) AS corr
FROM google_ads__campaign_report
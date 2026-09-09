SELECT 
  "Disaster Type",
  COUNT(*) AS cnt,
  ROUND(AVG(json_extract("Impact Indicator", '$.population.affected')),0) AS avg_affected,
  ROUND(AVG(fin."budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(tr."Daily Transport Volume (tons)"),0) AS avg_daily_vol
FROM disaster_events de
LEFT JOIN financials1 fin ON fin."Disaster Reference ID"=de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID"=de."Disaster Event ID"
WHERE de."Disaster Severity Level"='Level 5'
GROUP BY "Disaster Type"
ORDER BY cnt DESC
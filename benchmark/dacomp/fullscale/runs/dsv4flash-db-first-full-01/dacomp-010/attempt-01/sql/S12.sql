SELECT f."Season label",
  CASE WHEN strftime('%m', c."Transaction Date") IN ('03','04','05') THEN 'Spring'
       WHEN strftime('%m', c."Transaction Date") IN ('06','07','08') THEN 'Summer'
       WHEN strftime('%m', c."Transaction Date") IN ('09','10','11') THEN 'Autumn'
       ELSE 'Winter' END AS date_season,
  COUNT(*) AS n
FROM core_transaction_information c
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", date_season
ORDER BY f."Season label", date_season
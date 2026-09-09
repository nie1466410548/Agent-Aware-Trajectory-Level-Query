SELECT
  CASE WHEN "Promotion Date" <= '2025-07-03' THEN 'pre' ELSE 'gray' END AS period,
  Strategy,
  COUNT(*) AS rows,
  ROUND(SUM("Spend (Yuan)"),0) AS spend,
  SUM(Impressions) AS impressions,
  SUM(Clicks) AS clicks,
  ROUND(SUM(Clicks)*1.0/SUM(Impressions),4) AS ctr_w,
  ROUND(SUM("Spend (Yuan)")*1.0/SUM(Clicks),3) AS cpc_w,
  ROUND(SUM("Spend (Yuan)")*1000.0/SUM(Impressions),3) AS cpm_w,
  ROUND(AVG("Budget Utilization Rate"),4) AS budutil_avg
FROM sheet1
GROUP BY period, Strategy
ORDER BY Strategy, period
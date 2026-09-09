
  SELECT overall_performance_score, COUNT(*) AS n,
         ROUND(AVG(annual_spend_growth_pct),2) AS avg_growth,
         ROUND(MIN(annual_spend_growth_pct),2) AS min_growth,
         ROUND(MAX(annual_spend_growth_pct),2) AS max_growth
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  GROUP BY overall_performance_score ORDER BY overall_performance_score

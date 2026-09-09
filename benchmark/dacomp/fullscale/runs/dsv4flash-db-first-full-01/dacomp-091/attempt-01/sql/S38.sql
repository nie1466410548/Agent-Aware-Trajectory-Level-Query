
  SELECT vendor_tier, payment_risk_level, performance_rating, dependency_level, COUNT(*) AS n
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  GROUP BY vendor_tier, payment_risk_level, performance_rating, dependency_level
  ORDER BY n DESC

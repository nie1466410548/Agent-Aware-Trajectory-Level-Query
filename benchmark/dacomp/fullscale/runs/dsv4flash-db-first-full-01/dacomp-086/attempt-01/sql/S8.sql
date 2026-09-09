SELECT 
  PERCENTILE_25(days_since_last_activity) AS p25_days,
  PERCENTILE_50(days_since_last_activity) AS p50_days,
  PERCENTILE_75(days_since_last_activity) AS p75_days,
  PERCENTILE_25(total_activities_30d) AS p25_act,
  PERCENTILE_50(total_activities_30d) AS p50_act,
  PERCENTILE_75(total_activities_30d) AS p75_act,
  PERCENTILE_25(annual_revenue) AS p25_rev,
  PERCENTILE_50(annual_revenue) AS p50_rev,
  PERCENTILE_75(annual_revenue) AS p75_rev,
  PERCENTILE_25(total_won_amount) AS p25_won,
  PERCENTILE_50(total_won_amount) AS p50_won,
  PERCENTILE_75(total_won_amount) AS p75_won
FROM salesforce__customer_360_view
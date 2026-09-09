-- Search quality metrics by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS searches,
  ROUND(AVG(s."Input Duration"),1) AS avg_input_duration,
  ROUND(AVG(s."Viewed Result Count"),1) AS avg_viewed_results,
  ROUND(AVG(s."Clicked Result Count"),1) AS avg_clicked_results,
  ROUND(AVG(s."Search Conversion Rate"),3) AS avg_conv_rate,
  ROUND(AVG(s."Suggestion Count"),1) AS avg_suggestions,
  ROUND(SUM(s."No Result Search Count"),0) AS no_result_total,
  ROUND(AVG(s."Used Autocomplete" = 'Yes')*100,1) AS autocomplete_pct
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
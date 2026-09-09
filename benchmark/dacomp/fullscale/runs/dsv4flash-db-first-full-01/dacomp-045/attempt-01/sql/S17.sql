-- Get full search keyword distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, s."Search Keyword", COUNT(*) AS search_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, s."Search Keyword"
ORDER BY ug.user_group, search_count DESC
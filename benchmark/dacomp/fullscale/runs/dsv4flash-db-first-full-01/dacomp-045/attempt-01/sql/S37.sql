-- Search keyword preferences detailed: top keywords per user group with percentages
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
),
keyword_stats AS (
  SELECT ug.user_group, s."Search Keyword", COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct_in_group
  FROM user_groups ug
  JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
  GROUP BY ug.user_group, s."Search Keyword"
)
SELECT * FROM keyword_stats
WHERE user_group IN ('High-Value', 'Regular')
ORDER BY user_group, cnt DESC
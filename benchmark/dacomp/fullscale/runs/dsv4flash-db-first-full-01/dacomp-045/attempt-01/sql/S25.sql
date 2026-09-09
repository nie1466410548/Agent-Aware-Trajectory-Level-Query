-- Search behavior by day of week (0=Sunday, 6=Saturday)
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, CAST(strftime('%w', s."Search Time") AS INTEGER) AS day_of_week, COUNT(*) AS search_count
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, day_of_week
ORDER BY ug.user_group, day_of_week
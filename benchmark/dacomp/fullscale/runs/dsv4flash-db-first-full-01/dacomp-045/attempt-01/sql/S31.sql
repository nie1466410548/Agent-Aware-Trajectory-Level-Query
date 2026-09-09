-- Browsing brands by user group (views)
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Brand Name", COUNT(*) AS views,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
JOIN product_basic_information_table p ON b."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Brand Name"
ORDER BY ug.user_group, views DESC
-- Favorites by category and user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Category Name", COUNT(*) AS fav_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN product_favorites_table f ON ug."User ID" = f."User ID"
JOIN product_basic_information_table p ON f."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Category Name"
ORDER BY ug.user_group, fav_count DESC
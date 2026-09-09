-- Average price of browsed/favorited products by user group
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
  ROUND(AVG(p."Price"),2) AS avg_browsed_price,
  ROUND(AVG(p."Sale Price"),2) AS avg_browsed_sale_price,
  ROUND(AVG(p."Original Price"),2) AS avg_browsed_original_price
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
JOIN product_basic_information_table p ON b."Product ID" = p."Product ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
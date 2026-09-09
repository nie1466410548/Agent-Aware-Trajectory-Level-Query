-- Occupation distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Occupation", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Occupation"
ORDER BY ug.user_group, cnt DESC
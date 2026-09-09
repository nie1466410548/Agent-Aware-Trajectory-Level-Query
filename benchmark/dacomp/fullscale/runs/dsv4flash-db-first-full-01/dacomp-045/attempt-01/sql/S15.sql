-- Assign user groups: High-value (Diamond/Platinum), Regular, and Gold (intermediate)
SELECT u."User ID",
  CASE 
    WHEN u."Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
    WHEN u."Membership Level" = 'Regular' THEN 'Regular'
    ELSE 'Gold'
  END AS user_group
FROM user_basic_information_table u
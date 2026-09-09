SELECT 
  u."Age group",
  COUNT(DISTINCT c."Cart ID") as carts,
  SUM(CASE WHEN c."Is Checked Out"='Yes' THEN 1 ELSE 0 END) as checked_out,
  ROUND(100.0*SUM(CASE WHEN c."Is Checked Out"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as checkout_pct,
  ROUND(AVG(c."Number of Modifications"),2) as avg_mods,
  ROUND(AVG(c."Quantity Added"),2) as avg_qty
FROM user_basic_information_table_1 u
LEFT JOIN shopping_cart_operations_table c ON u."User ID"=c."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
SELECT c.gender,
  AVG(CAST(o.Discount AS REAL)) AS avg_discount,
  SUM(CASE WHEN CAST(o.Discount AS REAL) > 0 THEN 1 ELSE 0 END)*100.0/COUNT(*) AS pct_discounted,
  AVG(CAST(o."Shipping Cost" AS REAL)) AS avg_shipping_cost,
  o."Shipping Method", COUNT(*) AS orders
FROM order_information o JOIN customer_information c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Shipping Method"
ORDER BY c.gender, orders DESC
SELECT 
  SUM(CASE WHEN "Profit Margin" > 1 THEN 1 ELSE 0 END) AS rows_margin_gt1,
  SUM(CASE WHEN "Total Logistics Revenue" <= 0 THEN 1 ELSE 0 END) AS rows_rev_le0,
  SUM(CASE WHEN "Discount Amount" < 0 THEN 1 ELSE 0 END) AS rows_discount_neg,
  SUM(CASE WHEN "Total Logistics Cost" <= 0 THEN 1 ELSE 0 END) AS rows_cost_le0,
  COUNT(*) AS n
FROM sheet1 WHERE "Destination" LIKE 'South China%'
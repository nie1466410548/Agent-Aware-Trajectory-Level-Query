
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 'Low-Margin' ELSE 'Normal' END AS order_type
  FROM sheet1

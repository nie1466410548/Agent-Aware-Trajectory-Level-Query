WITH baskets AS (
  SELECT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)" AS basket_id,
         "Item Code"
  FROM sales_records
  WHERE strftime('%m', "Sales Date") = '07'
  GROUP BY basket_id, "Item Code"
)
SELECT basket_size, COUNT(*) AS n_baskets
FROM (SELECT basket_id, COUNT(*) AS basket_size FROM baskets GROUP BY basket_id)
GROUP BY basket_size ORDER BY n_baskets DESC LIMIT 20
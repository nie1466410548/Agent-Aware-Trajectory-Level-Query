WITH proc_items AS (
  SELECT DISTINCT s."Item Code", p."Item Name"
  FROM sales_records s
  LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
  WHERE date(s."Sales Date") = '2023-06-30'
)
SELECT pi."Item Code", pi."Item Name" FROM proc_items pi
ORDER BY pi."Item Code"
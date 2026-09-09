WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT pi."Item Code", p."Item Name"
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
WHERE pi."Item Code" NOT IN (SELECT "Item Code" FROM summer_items)
ORDER BY pi."Item Code"
SELECT s."Item Code", COUNT(*) as n_sales
FROM sales_records s
WHERE s."Item Code" IN (102900011018132, 102900011031926, 102900011035740, 102900011036686, 106971533450003)
  AND s."Sales type" = 'Sale'
  AND (
    (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
    OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
    OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
  )
GROUP BY s."Item Code"
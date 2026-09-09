SELECT COUNT(*) as cnt
FROM sales_records s
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01'
AND s."Sales type" = 'Sale'
AND pp."Wholesale price (yuan/kg)" IS NOT NULL
AND pl."Loss Rate (%)" IS NOT NULL
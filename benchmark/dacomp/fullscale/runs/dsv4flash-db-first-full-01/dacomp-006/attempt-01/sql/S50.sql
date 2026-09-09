WITH comp_month AS (
  SELECT strftime('%Y-%m',"Date") AS month,
    SUM("List Price Revenue") AS list_price,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Total Logistics Revenue") AS rev
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT month, ROUND(list_price,0) AS list_price, ROUND(vas,0) AS vas, ROUND(discount,0) AS discount,
  ROUND(list_price+vas-discount,0) AS calc_rev, ROUND(rev,0) AS actual_rev,
  ROUND(discount/(list_price+vas)*100,1) AS discount_rate_pct,
  ROUND(vas/(list_price+vas)*100,1) AS vas_share_pct
FROM comp_month ORDER BY month
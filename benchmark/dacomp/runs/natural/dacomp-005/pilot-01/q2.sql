SELECT "Total Logistics Revenue" AS rev, "Total Logistics Cost" AS cost, "Profit" AS profit,
"Profit Margin" AS margin,
ROUND("Profit"/"Total Logistics Revenue",4) AS pm_rev,
ROUND("Profit"/"Total Logistics Cost",4) AS pm_cost
FROM sheet1 LIMIT 10

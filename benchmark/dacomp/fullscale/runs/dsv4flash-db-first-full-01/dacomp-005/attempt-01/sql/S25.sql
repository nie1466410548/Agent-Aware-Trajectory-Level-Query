SELECT 
  "Date",
  "Sales Quantity",
  "Total Logistics Revenue",
  "Freight Cost",
  "Warehousing Cost",
  "Other Operating Costs",
  "Total Logistics Cost",
  "Discount Amount",
  "Profit",
  "Profit Margin",
  "Destination",
  "Consigned Product"
FROM sheet1 
WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
ORDER BY "Profit Margin" ASC
LIMIT 10
SELECT 
  MIN("Carat (diamond weight)") AS min_carat,
  MAX("Carat (diamond weight)") AS max_carat,
  MIN("Price (USD)") AS min_price,
  MAX("Price (USD)") AS max_price,
  ROUND(AVG("Carat (diamond weight)"),3) AS avg_carat,
  ROUND(AVG("Price (USD)"),2) AS avg_price,
  ROUND(AVG("Price (USD)"/"Carat (diamond weight)"),2) AS avg_ppc,
  ROUND(AVG("Depth percentage"),2) AS avg_depth,
  ROUND(AVG("Table percentage"),2) AS avg_table
FROM sheet1
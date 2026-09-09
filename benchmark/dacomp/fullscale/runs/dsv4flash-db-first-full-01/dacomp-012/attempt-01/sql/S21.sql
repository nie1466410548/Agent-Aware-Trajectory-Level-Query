WITH s AS (
  SELECT "Price (USD)" AS price, "Carat (diamond weight)" AS carat, "Depth percentage" AS depth,
         "Table percentage" AS tbl, "X-axis length (mm)" AS x, "Y-axis width (mm)" AS y, "Z-axis depth (mm)" AS z
  FROM sheet1
)
SELECT 'carat' AS var, ROUND((AVG(carat*price) - AVG(carat)*AVG(price)) / 
    (sqrt(AVG(carat*carat) - AVG(carat)*AVG(carat)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) AS corr_with_price
FROM s
UNION ALL
SELECT 'depth', ROUND((AVG(depth*price) - AVG(depth)*AVG(price)) / 
    (sqrt(AVG(depth*depth) - AVG(depth)*AVG(depth)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'table', ROUND((AVG(tbl*price) - AVG(tbl)*AVG(price)) / 
    (sqrt(AVG(tbl*tbl) - AVG(tbl)*AVG(tbl)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'x', ROUND((AVG(x*price) - AVG(x)*AVG(price)) / 
    (sqrt(AVG(x*x) - AVG(x)*AVG(x)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'y', ROUND((AVG(y*price) - AVG(y)*AVG(price)) / 
    (sqrt(AVG(y*y) - AVG(y)*AVG(y)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'z', ROUND((AVG(z*price) - AVG(z)*AVG(price)) / 
    (sqrt(AVG(z*z) - AVG(z)*AVG(z)) * sqrt(AVG(price*price) - AVG(price)*AVG(price))), 4) FROM s
UNION ALL
SELECT 'log(price) vs log(carat)', ROUND((AVG(ln(carat)*ln(price)) - AVG(ln(carat))*AVG(ln(price))) / 
    (sqrt(AVG(ln(carat)*ln(carat)) - AVG(ln(carat))*AVG(ln(carat))) * sqrt(AVG(ln(price)*ln(price)) - AVG(ln(price))*AVG(ln(price)))), 4) FROM s
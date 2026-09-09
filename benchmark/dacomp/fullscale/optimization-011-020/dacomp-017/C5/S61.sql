SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a3) AS "sales"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  yr,
  sales DESC;

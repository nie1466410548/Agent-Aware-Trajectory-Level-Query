WITH prod_month AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
),
cov AS (
  SELECT dim,
    SUM((p - (SELECT AVG(p) FROM prod_month p2 WHERE p2.dim=prod_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0 AS cov_p_t,
    (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) AS var_t
  FROM prod_month JOIN tot_month USING(month)
  GROUP BY dim
)
SELECT dim, ROUND(cov_p_t/var_t*100,1) AS variance_share_pct FROM cov ORDER BY variance_share_pct DESC
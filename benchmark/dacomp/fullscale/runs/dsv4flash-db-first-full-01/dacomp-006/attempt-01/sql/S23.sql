WITH age_month AS (
  SELECT "Age Range" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT dim,
  ROUND(SUM((p - (SELECT AVG(p) FROM age_month p2 WHERE p2.dim=age_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0
    / (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) * 100, 1) AS variance_share_pct
FROM age_month JOIN tot_month USING(month)
GROUP BY dim ORDER BY variance_share_pct DESC
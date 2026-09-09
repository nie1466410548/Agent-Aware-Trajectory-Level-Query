WITH monthly AS (
  SELECT country_short, sku_id, strftime('%Y-%m', date_day) AS month,
         SUM(net_amount) AS net, SUM(transactions) AS tx
  FROM google_play__finance_report
  WHERE package_name='com.dev.photoeditor'
  GROUP BY country_short, sku_id, month
),
first_last AS (
  SELECT country_short, sku_id,
    MIN(month) AS first_m, MAX(month) AS last_m,
    SUM(CASE WHEN month = (SELECT MIN(m2.month) FROM monthly m2 WHERE m2.country_short=monthly.country_short AND m2.sku_id=monthly.sku_id) THEN net END) AS first_net,
    SUM(CASE WHEN month = (SELECT MAX(m2.month) FROM monthly m2 WHERE m2.country_short=monthly.country_short AND m2.sku_id=monthly.sku_id) THEN net END) AS last_net
  FROM monthly
  GROUP BY country_short, sku_id
)
SELECT country_short, sku_id, first_m, last_m, ROUND(first_net,2) AS first_net, ROUND(last_net,2) AS last_net,
  ROUND((last_net-first_net)/first_net*100,1) AS pct_change
FROM first_last ORDER BY pct_change
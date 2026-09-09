SELECT
  PERCENTILE_25, PERCENTILE_50, PERCENTILE_75,
  AVG_C, MIN_C, MAX_C, STD_C
FROM (
  SELECT
    AVG(CASE WHEN pct <= 25 THEN comprehensive_customer_value END) AS PERCENTILE_25,
    AVG(CASE WHEN pct <= 50 THEN comprehensive_customer_value END) AS PERCENTILE_50,
    AVG(CASE WHEN pct <= 75 THEN comprehensive_customer_value END) AS PERCENTILE_75,
    AVG(comprehensive_customer_value) AS AVG_C,
    MIN(comprehensive_customer_value) AS MIN_C,
    MAX(comprehensive_customer_value) AS MAX_C,
    STDEV(comprehensive_customer_value) AS STD_C
  FROM (
    SELECT comprehensive_customer_value,
           NTILE(100) OVER (ORDER BY comprehensive_customer_value) AS pct
    FROM pendo__customer_lifecycle_insights
  )
) t
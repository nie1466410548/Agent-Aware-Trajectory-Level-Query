
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT * FROM la WHERE rn=1 LIMIT 3

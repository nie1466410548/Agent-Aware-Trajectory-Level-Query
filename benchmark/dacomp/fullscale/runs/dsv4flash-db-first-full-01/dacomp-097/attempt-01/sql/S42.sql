-- Percentile computation using window functions for outlier thresholds
WITH vals AS (
  SELECT 
    time_to_first_response_minutes AS resp_time,
    time_to_last_close_minutes AS duration
  FROM intercom__conversation_metrics
),
resp_pct AS (
  SELECT 
    resp_time,
    CUME_DIST() OVER (ORDER BY resp_time) AS cd
  FROM vals WHERE resp_time IS NOT NULL
),
dur_pct AS (
  SELECT 
    duration,
    CUME_DIST() OVER (ORDER BY duration) AS cd
  FROM vals WHERE duration IS NOT NULL
)
SELECT 
  (SELECT MIN(resp_time) FROM resp_pct WHERE cd >= 0.01) AS resp_p1,
  (SELECT MIN(resp_time) FROM resp_pct WHERE cd >= 0.99) AS resp_p99,
  (SELECT MIN(duration) FROM dur_pct WHERE cd >= 0.01) AS dur_p1,
  (SELECT MIN(duration) FROM dur_pct WHERE cd >= 0.99) AS dur_p99
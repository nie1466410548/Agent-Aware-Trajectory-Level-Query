-- Deduplicate: keep one row per lead, picking the one with highest rfm_avg_score
WITH dedup AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY marketo_lead_id ORDER BY rfm_avg_score DESC, rfm_score DESC) AS rn
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
)
SELECT * FROM dedup WHERE rn = 1
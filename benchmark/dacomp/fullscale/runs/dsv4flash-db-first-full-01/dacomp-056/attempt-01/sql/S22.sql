WITH lead_tiers AS (
  SELECT marketo_lead_id, COUNT(DISTINCT customer_tier) AS ntiers, COUNT(DISTINCT customer_segment) AS nsegs,
         COUNT(DISTINCT rfm_score) AS nrfm
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
  GROUP BY marketo_lead_id
)
SELECT SUM(CASE WHEN ntiers>1 THEN 1 ELSE 0 END) AS multi_tier_leads,
       SUM(CASE WHEN nsegs>1 THEN 1 ELSE 0 END) AS multi_seg_leads,
       SUM(CASE WHEN nrfm>1 THEN 1 ELSE 0 END) AS multi_rfm_leads,
       COUNT(*) AS total_leads
FROM lead_tiers
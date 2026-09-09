-- Check if customer360_id might be related to primary_email or marketo_lead_id
-- Let's see all unique source_systems and their counts
SELECT source_system, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
GROUP BY source_system
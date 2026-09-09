-- Check if there's a way to link address by looking at the frequency of customer360_id values
-- that match the count of distinct customer records
SELECT COUNT(DISTINCT customer360_id) AS total_ids,
       COUNT(*) AS total_rows
FROM customer360__address
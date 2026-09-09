-- Check if customer360_id might be a hash of email
SELECT primary_email, MD5(primary_email) FROM customer360__customer_activity_metrics LIMIT 5
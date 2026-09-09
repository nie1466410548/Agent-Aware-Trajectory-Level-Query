SELECT COUNT(DISTINCT v.stripe_customer_id) AS total_stripe_in_v
FROM customer360__customer_value_analysis v
WHERE v.stripe_customer_id IS NOT NULL
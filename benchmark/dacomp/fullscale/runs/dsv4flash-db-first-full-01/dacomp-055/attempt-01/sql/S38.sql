SELECT COUNT(DISTINCT v.stripe_customer_id) AS in_mapping
FROM customer360__customer_value_analysis v
WHERE v.stripe_customer_id IN (SELECT DISTINCT stripe_customer_id FROM customer360__mapping)
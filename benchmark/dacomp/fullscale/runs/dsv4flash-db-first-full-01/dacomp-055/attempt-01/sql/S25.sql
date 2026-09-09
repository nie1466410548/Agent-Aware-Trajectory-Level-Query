SELECT COUNT(*) AS matched_count
FROM customer360__customer_value_analysis v
JOIN customer360__customer c ON v.primary_email = c.email
LIMIT 10
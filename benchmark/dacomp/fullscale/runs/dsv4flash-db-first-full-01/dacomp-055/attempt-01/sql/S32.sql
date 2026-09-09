SELECT COUNT(*) AS email_match_count 
FROM (SELECT DISTINCT primary_email FROM customer360__customer_value_analysis) v
JOIN (SELECT DISTINCT email FROM customer360__customer) c ON v.primary_email = c.email
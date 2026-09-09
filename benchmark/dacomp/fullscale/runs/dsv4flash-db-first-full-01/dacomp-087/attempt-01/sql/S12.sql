SELECT owner_id, COUNT(DISTINCT billing_state) AS distinct_states, COUNT(DISTINCT billing_city) AS distinct_cities
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY distinct_states DESC
LIMIT 10
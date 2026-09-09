
SELECT c.visitor_id, c.comprehensive_customer_value, c.user_value_score
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id

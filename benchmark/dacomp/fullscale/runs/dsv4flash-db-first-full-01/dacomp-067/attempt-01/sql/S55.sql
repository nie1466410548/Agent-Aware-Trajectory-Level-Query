SELECT sourced_from, 
       AVG(julianday(last_activity_at) - julianday(applied_at)) as avg_days,
       MIN(julianday(last_activity_at) - julianday(applied_at)) as min_days,
       MAX(julianday(last_activity_at) - julianday(applied_at)) as max_days
FROM greenhouse__application_enhanced
WHERE last_activity_at IS NOT NULL AND applied_at IS NOT NULL
GROUP BY sourced_from
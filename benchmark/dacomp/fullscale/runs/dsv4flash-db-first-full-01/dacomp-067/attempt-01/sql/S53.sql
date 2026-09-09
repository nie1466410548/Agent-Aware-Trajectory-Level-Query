SELECT sourced_from, COUNT(*) as cnt,
       AVG(EXTRACT(EPOCH FROM (last_activity_at - applied_at))/86400.0) as avg_days
FROM greenhouse__application_enhanced
GROUP BY sourced_from
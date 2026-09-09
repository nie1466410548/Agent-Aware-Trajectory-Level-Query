SELECT sourced_from, COUNT(*) as cnt, 
       SUM(CASE WHEN source_id <= 8 THEN 1 ELSE 0 END) as mapped,
       MIN(source_id) as min_sid, MAX(source_id) as max_sid
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
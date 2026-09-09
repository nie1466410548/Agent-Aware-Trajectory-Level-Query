
SELECT sourced_from,
  COUNT(*) as apps,
  SUM(CASE WHEN count_interviews>0 THEN 1 ELSE 0 END) as interviewed,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced
GROUP BY sourced_from

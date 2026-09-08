SELECT COUNT(*) FILTER (WHERE closeddate IS NOT NULL) AS with_closed, COUNT(*) FILTER (WHERE status='Closed') AS closed_status, COUNT(DISTINCT status) FROM "Case" GROUP BY 1=1

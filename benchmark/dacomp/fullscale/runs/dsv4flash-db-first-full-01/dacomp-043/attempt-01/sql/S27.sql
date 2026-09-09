
SELECT "Shared Exposure History (Group Dining/Group Activity)" AS shared, COUNT(*) AS n FROM epidemiological_investigation GROUP BY shared ORDER BY n DESC;
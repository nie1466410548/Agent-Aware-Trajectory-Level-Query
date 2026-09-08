SELECT substr(createddate, 1, 7) AS month, COUNT(*) AS cnt
FROM "Case"
WHERE (subject ILIKE '%SecureAnalytics%' OR description ILIKE '%SecureAnalytics%')
AND createddate >= '2020-06-10' AND createddate <= '2021-04-10'
GROUP BY 1 ORDER BY 1;


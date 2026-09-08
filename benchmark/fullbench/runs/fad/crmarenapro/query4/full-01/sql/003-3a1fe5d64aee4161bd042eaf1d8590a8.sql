SELECT id, createddate, subject
FROM "Case"
WHERE (subject ILIKE '%SecureAnalytics%' OR description ILIKE '%SecureAnalytics%')
ORDER BY createddate;


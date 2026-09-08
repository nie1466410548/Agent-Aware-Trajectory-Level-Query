SELECT business_ref, COUNT(*) AS n, ROUND(AVG(rating),4) AS avg_r
FROM review
GROUP BY business_ref
ORDER BY business_ref;

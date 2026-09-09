SELECT title, COUNT(*) AS cnt FROM salesforce__contact_enhanced 
WHERE title IS NOT NULL
GROUP BY title ORDER BY cnt DESC LIMIT 100
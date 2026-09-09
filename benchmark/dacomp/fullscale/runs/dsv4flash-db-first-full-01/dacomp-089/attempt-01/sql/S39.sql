SELECT title, COUNT(*) AS cnt FROM salesforce__contact_enhanced 
WHERE title LIKE '%Vice%' OR title LIKE '%VP%' OR title LIKE '%President%' OR title LIKE '%Director%' 
   OR title LIKE '%Executive%' OR title LIKE '%Managing%' OR title LIKE '%Principal%' OR title LIKE '%Owner%'
GROUP BY title ORDER BY cnt DESC LIMIT 60
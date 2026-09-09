SELECT title, COUNT(*) AS cnt FROM salesforce__contact_enhanced 
WHERE LOWER(title) LIKE '%vice%' OR LOWER(title) LIKE '%v.p.%' OR LOWER(title) LIKE 'vp%' OR LOWER(title) LIKE '% svp%' OR LOWER(title) LIKE '%evp%'
GROUP BY title ORDER BY cnt DESC
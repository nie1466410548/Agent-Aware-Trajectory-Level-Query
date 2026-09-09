SELECT title, cnt FROM (
  SELECT title, COUNT(*) AS cnt FROM salesforce__contact_enhanced c
  WHERE c.account_id IN (
    SELECT a.account_id FROM salesforce__customer_360_view a WHERE a.annual_revenue >= 71234915
  ) AND c.title IS NOT NULL
  GROUP BY title
) WHERE title LIKE '%Chief%' OR title LIKE '%Executive%' OR title LIKE '%Director%' 
   OR title LIKE '%Manager%' OR title LIKE '%Head%' OR title LIKE '%President%'
   OR title LIKE '%VP%' OR title LIKE '%Vice%' OR title LIKE '%Officer%'
   OR title LIKE '%Owner%' OR title LIKE '%Partner%' OR title LIKE '%Principal%'
ORDER BY cnt DESC
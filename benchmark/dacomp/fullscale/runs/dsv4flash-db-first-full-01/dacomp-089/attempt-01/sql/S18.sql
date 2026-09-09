SELECT DISTINCT title FROM salesforce__contact_enhanced 
WHERE title IS NOT NULL 
  AND (LOWER(title) LIKE '%chief%' OR LOWER(title) LIKE '%vp%' OR LOWER(title) LIKE '%vice president%' 
       OR LOWER(title) LIKE '%president%' OR LOWER(title) LIKE '%director%' OR LOWER(title) LIKE '%executive%' 
       OR LOWER(title) LIKE '%owner%' OR LOWER(title) LIKE '%partner%' OR LOWER(title) LIKE '%principal%'
       OR LOWER(title) LIKE '%founder%' OR LOWER(title) LIKE '%chairman%' OR LOWER(title) LIKE '%head %'
       OR LOWER(title) LIKE '%managing director%')
ORDER BY title
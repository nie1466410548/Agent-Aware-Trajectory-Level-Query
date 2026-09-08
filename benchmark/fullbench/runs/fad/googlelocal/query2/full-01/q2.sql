SELECT gmap_id, name
FROM business_description
WHERE MISC::text ILIKE '%massage%'
  AND NOT (name ILIKE '%massage%' OR description ILIKE '%massage%')

SELECT name, gmap_id, description, hours
FROM business_description
WHERE description ILIKE '%Los Angeles%' OR hours ILIKE '%Los Angeles%'
LIMIT 10;

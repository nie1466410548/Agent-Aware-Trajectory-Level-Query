SELECT gmap_id, name, state, num_of_reviews
FROM business_description
WHERE name ILIKE '%massage%' OR description ILIKE '%massage%'

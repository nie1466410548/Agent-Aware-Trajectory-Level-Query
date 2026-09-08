SELECT track_id, title, artist FROM tracks
WHERE LOWER(TRIM(title)) LIKE '%street hype%' AND LOWER(TRIM(artist)) LIKE '%maginnis%';

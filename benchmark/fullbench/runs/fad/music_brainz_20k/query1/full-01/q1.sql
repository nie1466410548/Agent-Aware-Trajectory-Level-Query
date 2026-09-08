SELECT track_id, title, artist, album, year FROM tracks
WHERE title LIKE '%Get Me Bodied%' AND (artist LIKE '%Beyonc%' OR artist LIKE '%Beyonce%');

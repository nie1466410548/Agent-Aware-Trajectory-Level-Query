SELECT track_id, source_id, title, artist, album, year
FROM tracks
WHERE LOWER(title) = 'street hype'
  AND LOWER(artist) LIKE '%brucqe maginnis%';

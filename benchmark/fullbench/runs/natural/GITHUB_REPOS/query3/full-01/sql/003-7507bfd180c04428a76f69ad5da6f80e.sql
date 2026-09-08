SELECT language_description, COUNT(*) FROM languages GROUP BY language_description HAVING COUNT(*) < 200 LIMIT 50

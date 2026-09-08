SELECT language_description, COUNT(*) AS n FROM languages GROUP BY language_description ORDER BY n DESC LIMIT 30;

SELECT language_description, COUNT(*) AS n FROM languages WHERE lower(language_description) LIKE '%swift%' GROUP BY language_description ORDER BY n DESC LIMIT 20;


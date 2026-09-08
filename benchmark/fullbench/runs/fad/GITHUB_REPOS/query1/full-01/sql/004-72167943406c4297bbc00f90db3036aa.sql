SELECT COUNT(*) AS total, SUM(CASE WHEN language_description LIKE '%Python%' THEN 1 ELSE 0 END) AS with_python FROM languages

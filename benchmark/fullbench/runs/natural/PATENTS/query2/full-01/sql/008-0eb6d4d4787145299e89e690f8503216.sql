SELECT grant_date, COUNT(*) FROM publicationinfo WHERE Patents_info LIKE '% DE-%' AND grant_date LIKE '%2019%' GROUP BY grant_date LIMIT 30

SELECT substr(Patents_info, instr(Patents_info,'publication number'), 40) AS pn, COUNT(*) FROM publicationinfo GROUP BY pn ORDER BY COUNT(*) DESC LIMIT 10

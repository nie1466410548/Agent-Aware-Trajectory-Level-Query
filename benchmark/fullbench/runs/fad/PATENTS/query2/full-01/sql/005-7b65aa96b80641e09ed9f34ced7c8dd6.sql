SELECT COUNT(*) AS total, SUM(CASE WHEN Patents_info LIKE '%DE-%' THEN 1 ELSE 0 END) AS de_pub, SUM(CASE WHEN Patents_info LIKE '%US-%' THEN 1 ELSE 0 END) AS us_pub FROM publicationinfo

SELECT "Promotion Date", COUNT(*) AS n, COUNT(DISTINCT "Promotion Tertiary Category") AS n_cat
FROM sheet1 WHERE Strategy='Search Strategy v3.6'
GROUP BY "Promotion Date" ORDER BY "Promotion Date"
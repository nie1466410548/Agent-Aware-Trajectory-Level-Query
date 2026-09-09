SELECT 'Gender' AS col, Gender AS val, COUNT(*) AS n FROM sheet1 GROUP BY Gender
UNION ALL
SELECT 'Part-time job', "Part-time job", COUNT(*) FROM sheet1 GROUP BY "Part-time job"
UNION ALL
SELECT 'Diet quality', "Diet quality", COUNT(*) FROM sheet1 GROUP BY "Diet quality"
UNION ALL
SELECT 'Internet quality', "Internet quality", COUNT(*) FROM sheet1 GROUP BY "Internet quality"
UNION ALL
SELECT 'Extracurricular', "Extracurricular activity participation", COUNT(*) FROM sheet1 GROUP BY "Extracurricular activity participation"
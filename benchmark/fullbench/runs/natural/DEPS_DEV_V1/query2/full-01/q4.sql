SELECT COUNT(*) AS total,
SUM(CASE WHEN Licenses LIKE '%"MIT"%' THEN 1 ELSE 0 END) AS mit_cnt
FROM packageinfo WHERE System='NPM';

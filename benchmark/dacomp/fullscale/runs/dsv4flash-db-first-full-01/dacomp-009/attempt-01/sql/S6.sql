SELECT 'sheet1' AS tbl, MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(DISTINCT "Employee") AS employees FROM sheet1
UNION ALL
SELECT 'sheet2', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet2
UNION ALL
SELECT 'sheet3', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet3
UNION ALL
SELECT 'sheet4', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet4
UNION ALL
SELECT 'sheet5', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet5
UNION ALL
SELECT 'sheet6', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet6
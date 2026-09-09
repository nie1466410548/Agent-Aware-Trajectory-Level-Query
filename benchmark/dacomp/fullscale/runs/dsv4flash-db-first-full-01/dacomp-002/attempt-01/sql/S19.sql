
SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"

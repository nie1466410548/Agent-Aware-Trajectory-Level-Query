
SELECT "Major Category Name", "Is Promotional", ROUND(SUM("Sales Amount"),2) AS total_amount, COUNT(*) AS n
FROM sheet1
GROUP BY "Major Category Name", "Is Promotional"

SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", MIN("Sales Amount") AS min_amt, MAX("Sales Amount") AS max_amt, ROUND(AVG("Sales Amount"),2) AS avg_amt, COUNT(*) AS n
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code"
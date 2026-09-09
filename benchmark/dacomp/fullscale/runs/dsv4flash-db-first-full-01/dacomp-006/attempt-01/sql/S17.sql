SELECT 
  substr("Destination", 13, instr("Destination", '-', 13) - 13) AS province,
  COUNT(*) AS n,
  SUM("Profit") AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province
ORDER BY profit DESC
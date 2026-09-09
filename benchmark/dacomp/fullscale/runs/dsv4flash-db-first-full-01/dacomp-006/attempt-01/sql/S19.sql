SELECT 
  substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province,
  COUNT(*) AS n,
  ROUND(SUM("Profit"),0) AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province
ORDER BY profit DESC
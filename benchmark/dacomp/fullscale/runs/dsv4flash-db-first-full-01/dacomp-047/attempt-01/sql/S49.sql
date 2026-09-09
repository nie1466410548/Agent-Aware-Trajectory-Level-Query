-- Monthly 2023 trend for top 2023 items
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date" >= '2022-10-01'
  AND s."Item Code" IN (
    106949711300259,102900011030059,102900011031100,102900011016701,
    102900011032251,102900011030097,102900005118831,102900005116714,
    102900011034231,102900011030110,102900005116257,102900011034330
  )
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym

    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july_vol,
           ROUND(SUM(s."Sales volume (kg)"),1) AS total_vol,
           ROUND(COUNT(DISTINCT s."Sales Date")*1.0/1096,4) AS freq,
           ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)"*s."Unit price (yuan/kg)" ELSE 0 END),0) AS july_revenue
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name"

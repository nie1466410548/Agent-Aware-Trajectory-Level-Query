
    SELECT s."Item Code" AS code, 
           ROUND(AVG(s."Unit price (yuan/kg)") - AVG(pp."Wholesale price (yuan/kg)"),2) AS margin
    FROM sales_records s
    LEFT JOIN purchase_price pp ON s."Item Code"=pp."Item Code" AND date(s."Sales Date")=date(pp."Date")
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code"

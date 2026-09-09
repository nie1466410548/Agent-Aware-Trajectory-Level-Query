
    SELECT strftime('%Y-%m-%d', s."Sales Date") AS d, s."Item Code", pi."Item Name", SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY d, s."Item Code", pi."Item Name"
    ORDER BY d, pi."Item Name"

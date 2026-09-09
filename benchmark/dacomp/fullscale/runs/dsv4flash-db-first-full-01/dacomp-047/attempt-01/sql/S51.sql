
    SELECT pi."Item Name" AS name, strftime('%Y-%m', s."Sales Date") AS ym,
           SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Sales Date" >= '2022-10-01'
    GROUP BY pi."Item Name", ym
    HAVING SUM(s."Sales volume (kg)") > 50
    ORDER BY pi."Item Name", ym

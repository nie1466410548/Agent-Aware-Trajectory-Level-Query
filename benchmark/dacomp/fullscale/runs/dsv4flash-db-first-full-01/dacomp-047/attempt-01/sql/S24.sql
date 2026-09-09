
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo

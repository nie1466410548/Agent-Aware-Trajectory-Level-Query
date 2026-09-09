SELECT date("Sales Date") as d, "Unit price (yuan/kg)", "Sales volume (kg)", "Whether sold at a discount"
FROM sales_records WHERE "Item Code" = 102900005118824 AND date("Sales Date") = '2023-06-30'
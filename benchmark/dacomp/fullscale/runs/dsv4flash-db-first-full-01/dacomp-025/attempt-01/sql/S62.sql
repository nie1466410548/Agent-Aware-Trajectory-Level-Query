SELECT date("Sales Date") as d, "Unit price (yuan/kg)", "Sales volume (kg)", "Whether sold at a discount"
FROM sales_records WHERE "Item Code" = 102900011032732 AND date("Sales Date") = '2023-06-30'
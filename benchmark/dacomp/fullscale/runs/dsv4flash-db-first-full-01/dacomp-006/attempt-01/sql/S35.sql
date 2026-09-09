SELECT "Waybill Number", "Date", "Destination", "Consigned Product", "Sales Quantity", 
  "Total Logistics Revenue", "Total Logistics Cost", "Profit", "Profit Margin"
FROM sheet1 WHERE "Destination" LIKE 'South China%'
ORDER BY "Profit" DESC LIMIT 15
-- Purchase price info for top July items
SELECT pp."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) AS avg_wholesale,
       ROUND(AVG(CASE WHEN strftime('%m', pp."Date")='07' THEN pp."Wholesale price (yuan/kg)" END),2) AS july_wholesale
FROM purchase_price pp
JOIN product_information pi ON pp."Item Code"=pi."Item Code"
GROUP BY pp."Item Code", pi."Item Name", pi."Category Name"
ORDER BY pi."Item Code"
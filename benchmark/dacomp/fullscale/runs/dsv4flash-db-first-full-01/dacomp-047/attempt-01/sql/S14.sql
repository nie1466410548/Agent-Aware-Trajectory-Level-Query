SELECT COUNT(DISTINCT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)") AS n_baskets,
       COUNT(*) AS n_rows,
       COUNT(*)*1.0 / COUNT(DISTINCT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)") AS avg_items_per_basket
FROM sales_records
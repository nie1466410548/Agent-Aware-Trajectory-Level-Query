WITH rfm AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
),
scored AS (
  SELECT "Customer ID",
         NTILE(4) OVER (ORDER BY julianday('2024-12-31') - julianday(last_order) DESC) AS R,
         NTILE(4) OVER (ORDER BY frequency ASC) AS F,
         NTILE(4) OVER (ORDER BY monetary ASC) AS M
  FROM rfm
)
SELECT CASE WHEN R+F+M >= 10 THEN 'Top Tier'
            WHEN R+F+M >= 7 THEN 'Mid Tier'
            WHEN R+F+M >= 4 THEN 'Low Tier'
            ELSE 'Bottom Tier' END AS segment,
       COUNT(*) AS n_customers
FROM scored
GROUP BY segment
ORDER BY n_customers DESC
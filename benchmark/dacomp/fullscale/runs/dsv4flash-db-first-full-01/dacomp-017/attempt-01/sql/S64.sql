
SELECT pb."Customer ID", pb."Product Category", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Customer ID"

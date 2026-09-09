SELECT pb."Product Category", pb."Product",
       COUNT(*) AS n,
       SUM(pb."like") AS total_likes,
       SUM(pb."share") AS total_shares,
       SUM(pb."Add to Cart") AS total_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Product"
ORDER BY n DESC
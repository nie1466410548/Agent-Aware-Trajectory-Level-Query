-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c10" AS
SELECT * FROM "product_browsing" WHERE "Product Category" = 'Home & Furniture';

-- S40
SELECT
  pb."Product Category" AS "Product Category",
  pb."Product" AS "Product",
  AVG(pb."Browsing Time (minutes)") AS "avg_browsing",
  AVG(pb."like") AS "avg_like",
  AVG(pb."share") AS "avg_share",
  AVG(pb."Add to Cart") AS "avg_add_to_cart"
FROM temp."reuse_017_c10" AS pb
WHERE
  pb."Product Category" = 'Home & Furniture'
GROUP BY
  pb."Product"
ORDER BY
  avg_browsing DESC;

-- S41
SELECT
  pb."Product Category" AS "Product Category",
  pb."Product" AS "Product",
  COUNT(*) AS "n",
  SUM(pb."like") AS "total_likes",
  SUM(pb."share") AS "total_shares",
  SUM(pb."Add to Cart") AS "total_add_to_cart"
FROM temp."reuse_017_c10" AS pb
WHERE
  pb."Product Category" = 'Home & Furniture'
GROUP BY
  pb."Product"
ORDER BY
  n DESC;

-- S64
SELECT
  pb."Customer ID" AS "Customer ID",
  pb."Product Category" AS "Product Category",
  AVG(pb."Browsing Time (minutes)") AS "avg_browsing",
  AVG(pb."like") AS "avg_like",
  AVG(pb."share") AS "avg_share",
  AVG(pb."Add to Cart") AS "avg_add_to_cart"
FROM temp."reuse_017_c10" AS pb
WHERE
  pb."Product Category" = 'Home & Furniture'
GROUP BY
  pb."Customer ID";

DROP TABLE temp."reuse_017_c10";

SELECT
  profit AS "profit",
  Sales AS "Sales",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin",
  Sales - profit AS "cost",
  "Quantity" AS "Quantity",
  "Shipping Cost" AS "Shipping Cost"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
LIMIT 20;

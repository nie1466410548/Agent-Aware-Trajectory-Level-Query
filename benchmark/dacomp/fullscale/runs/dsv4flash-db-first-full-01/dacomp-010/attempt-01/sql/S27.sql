
SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty,
       c."Unit Price (yuan)" AS price,
       c."Total Transaction Amount" AS amount,
       c."Buyer Type" AS buyer,
       c."Promotion" AS promo,
       f."Customer Satisfaction" AS sat,
       f."Repurchase intention" AS repur
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'

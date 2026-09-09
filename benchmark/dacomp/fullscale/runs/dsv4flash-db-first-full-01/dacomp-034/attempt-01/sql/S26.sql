SELECT 
  MIN(pdj_price) AS min_pdj, 
  MAX(pdj_price) AS max_pdj, 
  MIN(promotion_price) AS min_promo, 
  MAX(promotion_price) AS max_promo,
  MIN(1.0 - promotion_price / pdj_price) AS min_dd,
  MAX(1.0 - promotion_price / pdj_price) AS max_dd,
  AVG(1.0 - promotion_price / pdj_price) AS avg_dd
FROM attachment_3 
WHERE promotion_type = 4 AND state = 5 AND pdj_price > 0
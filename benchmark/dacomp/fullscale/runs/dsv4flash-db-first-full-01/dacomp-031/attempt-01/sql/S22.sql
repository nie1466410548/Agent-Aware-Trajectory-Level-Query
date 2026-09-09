SELECT Attrition,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END)*100,2) AS pct_promo_0_1yr,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END)*100,2) AS pct_promo_2_3yr,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion >= 4 THEN 1 ELSE 0 END)*100,2) AS pct_promo_4plus_yr
FROM sheet1
GROUP BY Attrition
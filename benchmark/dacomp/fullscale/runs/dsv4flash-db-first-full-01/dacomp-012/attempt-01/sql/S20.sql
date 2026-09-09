SELECT 
  ROUND(AVG("Carat (diamond weight)" * "Price (USD)") - AVG("Carat (diamond weight)") * AVG("Price (USD)"), 4) AS carat_price_cov,
  ROUND((AVG("Carat (diamond weight)" * "Price (USD)") - AVG("Carat (diamond weight)") * AVG("Price (USD)")) / 
    (sqrt(AVG("Carat (diamond weight)"*"Carat (diamond weight)") - AVG("Carat (diamond weight)")*AVG("Carat (diamond weight)")) * 
     sqrt(AVG("Price (USD)"*"Price (USD)") - AVG("Price (USD)")*AVG("Price (USD)"))), 4) AS corr_carat_price
FROM sheet1
SELECT subject_keyword, 
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_placed_orders), 1) AS avg_orders,
       ROUND(AVG(gmv_net), 1) AS avg_gmv,
       COUNT(*) AS n
FROM (
  SELECT
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate, total_placed_orders, gmv_net
  FROM klaviyo__campaigns
)
GROUP BY subject_keyword
ORDER BY avg_open DESC
SELECT variation_id, COUNT(*) AS n_persons,
       ROUND(AVG(count_viewed_product),2) AS avg_views,
       ROUND(AVG(count_placed_order),2) AS avg_orders,
       ROUND(AVG(net_revenue_touch),2) AS avg_net_rev,
       ROUND(AVG(email_open_rate_touch),4) AS avg_open_touch,
       ROUND(AVG(email_click_to_open_rate_touch),4) AS avg_ctor_touch,
       ROUND(SUM(has_converted)*100.0/COUNT(*),2) AS conv_pct
FROM klaviyo__person_campaign_flow
GROUP BY variation_id
ORDER BY variation_id
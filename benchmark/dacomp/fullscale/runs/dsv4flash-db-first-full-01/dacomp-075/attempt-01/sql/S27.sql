SELECT vendor_category_name, COUNT(*) AS n, ROUND(SUM(total_vendor_spend),0) AS total_spend,
       ROUND(AVG(avg_payment_delay),1) AS avg_delay_days, ROUND(AVG(overdue_payment_percentage),1) AS avg_overdue_pct,
       ROUND(AVG(financial_health_score),1) AS avg_fin_health, ROUND(AVG(cybersecurity_score),1) AS avg_cyber,
       ROUND(AVG(quality_score),1) AS avg_quality, ROUND(AVG(innovation_capability_score),1) AS avg_innovation,
       ROUND(AVG(market_volatility_index),3) AS avg_mkt_vol, ROUND(AVG(price_volatility_coefficient),3) AS avg_price_vol
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY vendor_category_name
ORDER BY total_spend DESC
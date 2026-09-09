SELECT geographic_region, COUNT(*) AS vendor_count, ROUND(SUM(total_vendor_spend),0) AS total_spend,
       ROUND(SUM(total_vendor_spend)/SUM(SUM(total_vendor_spend)) OVER ()*100,1) AS spend_pct
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY geographic_region
ORDER BY total_spend DESC
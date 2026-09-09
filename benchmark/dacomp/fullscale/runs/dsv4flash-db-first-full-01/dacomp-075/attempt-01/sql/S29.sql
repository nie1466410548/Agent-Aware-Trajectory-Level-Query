SELECT dependency_level, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY dependency_level ORDER BY n DESC
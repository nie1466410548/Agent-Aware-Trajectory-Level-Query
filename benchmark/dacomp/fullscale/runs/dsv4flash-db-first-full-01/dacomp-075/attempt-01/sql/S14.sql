SELECT
  SUM(CASE WHEN spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical','High Strategic Value') THEN 1 ELSE 0 END) AS focus_group_count,
  SUM(CASE WHEN spend_concentration_ratio > 0.15 THEN 1 ELSE 0 END) AS conc_gt15,
  SUM(CASE WHEN strategic_importance_level IN ('Mission Critical','High Strategic Value') THEN 1 ELSE 0 END) AS strat_high
FROM netsuite2_vendor_risk_analysis
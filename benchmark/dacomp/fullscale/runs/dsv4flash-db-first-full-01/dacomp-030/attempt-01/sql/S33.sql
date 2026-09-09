WITH pos_agg AS (
  SELECT p."Outlet Type",
    COUNT(DISTINCT p."Outlet ID") AS num_outlets,
    ROUND(SUM(p."Actual Sales (cases)") * 1.0 / NULLIF(SUM(p."Sales Target"), 0), 4) AS pos_target_ach,
    ROUND(AVG(p."VPO Value"), 3) AS avg_vpo,
    ROUND(AVG(p."PC Value"), 1) AS avg_pc,
    ROUND(AVG(CAST(REPLACE(p."Qualification Rate", '%', '') AS REAL)), 2) AS avg_qual_rate
  FROM "point_of_sale_(pos)_information" p
  GROUP BY p."Outlet Type"
),
sales_agg AS (
  SELECT p."Outlet Type",
    ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_tar,
    ROUND(AVG(s." YoY Growth Rate"), 2) AS avg_yoy,
    ROUND(AVG(s."MoM Growth Rate"), 2) AS avg_mom,
    ROUND(SUM(s."Sales (Value)"), 0) AS total_sales_value,
    ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value
  FROM "point_of_sale_(pos)_information" p
  JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
  GROUP BY p."Outlet Type"
),
contract_agg AS (
  SELECT p."Outlet Type",
    COUNT(c."Agreement ID") AS num_contracts,
    ROUND(SUM(c."Signing Amount (CNY)"), 0) AS total_signing_amount,
    ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_signing_amount,
    ROUND(AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END), 3) AS renewal_ratio
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
  GROUP BY p."Outlet Type"
),
mgmt_agg AS (
  SELECT p."Outlet Type",
    ROUND(SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS complaint_ratio,
    ROUND(SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS quality_ratio,
    SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID") AS renew_high_ratio
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
  GROUP BY p."Outlet Type"
),
assess_agg AS (
  SELECT p."Outlet Type",
    ROUND(AVG(a."Assessment pass rate"), 4) AS avg_pass_rate,
    ROUND(AVG(a."Score"), 2) AS avg_score
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
  GROUP BY p."Outlet Type"
),
appeal_agg AS (
  SELECT p."Outlet Type",
    COUNT(ap."Appeal ID") * 1.0 / COUNT(DISTINCT p."Outlet ID") AS appeals_per_outlet
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN appeal_record_table ap ON p."Outlet ID" = ap."Outlet ID"
  GROUP BY p."Outlet Type"
)
SELECT pa."Outlet Type", pa.num_outlets, pa.pos_target_ach, pa.avg_vpo, pa.avg_pc, pa.avg_qual_rate,
  sa.avg_tar, sa.avg_yoy, sa.avg_mom, sa.total_sales_value, sa.avg_sales_value,
  ca.num_contracts, ca.total_signing_amount, ca.avg_signing_amount, ca.renewal_ratio,
  ma.complaint_ratio, ma.quality_ratio, ma.renew_high_ratio,
  aa.avg_pass_rate, aa.avg_score, ap.appeals_per_outlet
FROM pos_agg pa
LEFT JOIN sales_agg sa ON pa."Outlet Type" = sa."Outlet Type"
LEFT JOIN contract_agg ca ON pa."Outlet Type" = ca."Outlet Type"
LEFT JOIN mgmt_agg ma ON pa."Outlet Type" = ma."Outlet Type"
LEFT JOIN assess_agg aa ON pa."Outlet Type" = aa."Outlet Type"
LEFT JOIN appeal_agg ap ON pa."Outlet Type" = ap."Outlet Type"
ORDER BY pa.num_outlets DESC
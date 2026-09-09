SELECT p."Outlet Type",
  COUNT(a."Assessment ID") AS n_assessments,
  ROUND(AVG(a."Score"), 2) AS avg_score,
  ROUND(AVG(a."Assessment pass rate"), 4) AS avg_pass_rate,
  ROUND(AVG(a."Historical pass trend (%)"), 2) AS avg_hist_pass_trend,
  ROUND(AVG(a."Photo upload count"), 2) AS avg_photo_upload,
  ROUND(AVG(a."Qualified photo count"), 2) AS avg_qualified_photo,
  ROUND(AVG(a."Qualified photo count" * 1.0 / NULLIF(a."Photo upload count", 0)), 4) AS photo_qual_rate
FROM "point_of_sale_(pos)_information" p
LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_pass_rate

SELECT
  SUM(CASE WHEN "Medical history" IS NULL THEN 1 ELSE 0 END) AS mhx_null,
  SUM(CASE WHEN "Health status" IS NULL THEN 1 ELSE 0 END) AS hs_null,
  SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END) AS id_null
FROM health_status

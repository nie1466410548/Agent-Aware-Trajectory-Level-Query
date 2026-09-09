SELECT COUNT(*) AS n_total,
  SUM(CASE WHEN created_at >= '2023-02-27' THEN 1 ELSE 0 END) AS n_last6mo
FROM klaviyo__flows
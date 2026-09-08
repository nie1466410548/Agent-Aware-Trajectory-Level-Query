SELECT "Index",
       COUNT(*) AS n_days,
       AVG((High - Low) / Close) AS avg_hl_close,
       AVG((High - Low) / Open) AS avg_hl_open,
       AVG(High - Low) AS avg_hl_abs
FROM index_trade
WHERE Date >= '2020-01-01'
  AND "Index" IN ('N225','NSEI','HSI','000001.SS','399001.SZ','TWII')
GROUP BY "Index"
ORDER BY avg_hl_close DESC;

(SELECT level, symbol, parents FROM cpc_definition WHERE level = 5 ORDER BY symbol LIMIT 8)
UNION ALL
(SELECT level, symbol, parents FROM cpc_definition WHERE level = 7 ORDER BY symbol LIMIT 8)
UNION ALL
(SELECT level, symbol, parents FROM cpc_definition WHERE level = 8 ORDER BY symbol LIMIT 8);

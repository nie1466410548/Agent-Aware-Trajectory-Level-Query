SELECT level, COUNT(*) AS n, MIN(symbol) AS example FROM cpc_definition GROUP BY level ORDER BY level

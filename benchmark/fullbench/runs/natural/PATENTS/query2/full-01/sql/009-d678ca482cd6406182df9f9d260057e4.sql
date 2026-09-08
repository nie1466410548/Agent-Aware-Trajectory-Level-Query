SELECT level, COUNT(*), MIN(symbol), MAX(symbol) FROM cpc_definition GROUP BY level ORDER BY level

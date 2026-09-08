SELECT "Index", Date, Open, High, Low, Close
FROM index_trade
WHERE "Index" IN ('N225','NSEI','HSI','000001.SS','399001.SZ','TWII');


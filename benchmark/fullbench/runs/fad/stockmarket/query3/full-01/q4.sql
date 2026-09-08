SELECT 'AGMH' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "AGMH" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'AMTX' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "AMTX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'APEX' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "APEX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'BIOC' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "BIOC" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'BKYI' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "BKYI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CBAT' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "CBAT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CCCL' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "CCCL" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CORV' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "CORV" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CPAH' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "CPAH" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'DZSI' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "DZSI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FAMI' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "FAMI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FTFT' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "FTFT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FTR' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "FTR" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'IDEX' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "IDEX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'ISDS' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "ISDS" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'MCEP' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "MCEP" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'NXTD' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "NXTD" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'OPTT' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "OPTT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'PEIX' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "PEIX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'RBZ' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "RBZ" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SES' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "SES" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SNSS' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "SNSS" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SPI' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "SPI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SYPR' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "SYPR" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'VTIQW' AS symbol, AVG("Volume") AS avg_volume, COUNT("Volume") AS n_days FROM "VTIQW" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
ORDER BY symbol;
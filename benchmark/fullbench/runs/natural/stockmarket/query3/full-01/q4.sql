SELECT 'AGMH' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "AGMH" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'AMTX' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "AMTX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'APEX' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "APEX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'BIOC' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "BIOC" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'BKYI' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "BKYI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CBAT' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "CBAT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CCCL' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "CCCL" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CORV' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "CORV" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'CPAH' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "CPAH" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'DZSI' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "DZSI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FAMI' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "FAMI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FTFT' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "FTFT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'FTR' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "FTR" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'IDEX' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "IDEX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'ISDS' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "ISDS" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'MCEP' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "MCEP" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'NXTD' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "NXTD" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'OPTT' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "OPTT" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'PEIX' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "PEIX" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'RBZ' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "RBZ" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SES' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "SES" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SNSS' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "SNSS" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SPI' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "SPI" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'SYPR' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "SYPR" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
UNION ALL
SELECT 'VTIQW' AS symbol, COUNT(*) AS days_2008, AVG("Volume") AS avg_volume_2008 FROM "VTIQW" WHERE "Date" >= '2008-01-01' AND "Date" <= '2008-12-31'
ORDER BY symbol;
SELECT 'AEFC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AEFC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AIN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AIN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AIV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AIV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AIZP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AIZP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AJRD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AJRD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AMN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AMN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AMP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AMP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AMT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AMT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ARD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ARD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ARGD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ARGD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ARLO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ARLO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ASG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ASG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'AVA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "AVA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BANC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BANC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BBU' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BBU" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BBVA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BBVA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BDXA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BDXA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BKH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BKH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BKT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BKT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BLD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BLD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BNS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BNS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'BZH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "BZH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CADE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CADE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CAE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CAE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CAF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CAF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CBT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CBT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CCC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CCC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CCZ' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CCZ" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CHAP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CHAP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CIA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CIA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CMA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CMA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CMI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CMI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CMSA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CMSA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CNK' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CNK" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'COTY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "COTY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CRC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CRC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CRM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CRM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CRS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CRS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CSL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CSL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CTS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CTS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CUBE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CUBE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CURO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CURO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CVIA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CVIA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CVX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CVX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'CXH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "CXH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DAC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DAC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DDS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DDS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DDT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DDT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DEO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DEO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DGX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DGX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DMB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DMB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DTQ' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DTQ" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'DXC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "DXC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EARN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EARN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EBS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EBS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EGO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EGO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EGY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EGY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EIG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EIG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ELF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ELF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EMP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EMP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ENLC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ENLC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EPR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EPR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EPRT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EPRT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ES' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ES" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ESRT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ESRT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ESS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ESS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ETM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ETM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EVT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EVT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'EXP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "EXP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'FMN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "FMN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'FPAC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "FPAC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'FSM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "FSM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GCO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GCO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GDL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GDL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GDV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GDV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GEL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GEL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GJP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GJP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GLOB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GLOB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GLT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GLT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GOL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GOL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GSLD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GSLD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GTY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GTY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GVA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GVA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'GWB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "GWB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'H' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "H" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HBI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HBI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HDB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HDB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HEP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HEP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HIL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HIL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HIO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HIO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HIX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HIX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HLF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HLF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HLT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HLT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HNI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HNI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HRB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HRB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'HTFA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "HTFA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IBM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IBM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IGR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IGR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IHC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IHC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IPG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IPG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IRM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IRM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'IT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "IT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'JGH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "JGH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'JHY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "JHY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'JKS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "JKS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'JMP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "JMP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'JNPR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "JNPR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'KMB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "KMB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'KNX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "KNX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'KW' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "KW" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'KYN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "KYN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'LB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "LB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'LDOS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "LDOS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'LHC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "LHC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'LHX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "LHX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'LOMA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "LOMA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MANU' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MANU" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MDLX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MDLX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MDLY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MDLY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MED' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MED" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MFO' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MFO" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MGR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MGR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MGU' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MGU" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MHE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MHE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MIY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MIY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MKC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MKC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MLI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MLI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MNE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MNE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MTD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MTD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'MYD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "MYD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NFH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NFH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NGG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NGG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NJV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NJV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NNI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NNI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NNY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NNY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NRUC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NRUC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NUE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NUE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'NXN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "NXN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'OCFT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "OCFT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'OEC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "OEC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ORA' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ORA" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ORAN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ORAN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ORCL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ORCL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ORN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ORN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PAG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PAG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PBI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PBI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PFE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PFE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PFSI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PFSI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PGR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PGR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PIM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PIM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PKE' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PKE" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PLAN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PLAN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PLNT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PLNT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PMT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PMT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PNM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PNM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PPG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PPG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PRSP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PRSP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PRTY' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PRTY" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PSV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PSV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'PSXP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "PSXP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'QTS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "QTS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'QUAD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "QUAD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RBC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RBC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RCB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RCB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RCI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RCI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RES' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RES" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'REXR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "REXR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RMT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RMT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ROG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ROG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ROL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ROL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RPAI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RPAI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RPM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RPM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RQI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RQI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'RWT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "RWT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SAF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SAF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SAIL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SAIL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SAM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SAM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SBR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SBR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SCU' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SCU" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SFUN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SFUN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SHAK' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SHAK" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SITC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SITC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SJM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SJM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SJT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SJT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SJW' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SJW" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SLF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SLF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SMP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SMP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SOL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SOL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SPOT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SPOT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SRC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SRC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SRF' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SRF" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SRT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SRT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SSD' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SSD" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'STG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "STG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'STL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "STL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'STON' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "STON" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'SYX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "SYX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TBB' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TBB" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TCP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TCP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TDJ' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TDJ" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TGP' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TGP" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TLYS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TLYS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TNC' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TNC" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TPH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TPH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TRV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TRV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TTI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TTI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TUFN' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TUFN" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'TWTR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "TWTR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'UHT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "UHT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'UIS' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "UIS" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'USX' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "USX" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'UTL' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "UTL" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VET' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VET" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VGR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VGR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VHI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VHI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VIV' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VIV" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VKQ' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VKQ" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VRT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VRT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'VVI' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "VVI" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'WOR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "WOR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'WPG' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "WPG" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'WSM' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "WSM" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'X' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "X" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'YEXT' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "YEXT" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ZNH' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ZNH" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'
UNION ALL
SELECT 'ZTR' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "ZTR" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'

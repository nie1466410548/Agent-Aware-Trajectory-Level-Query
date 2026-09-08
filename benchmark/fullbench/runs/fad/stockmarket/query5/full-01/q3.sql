SELECT symbol, days FROM (
SELECT 'AGMH' AS symbol, COUNT(*) AS days FROM "AGMH" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ALACU' AS symbol, COUNT(*) AS days FROM "ALACU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'AMHC' AS symbol, COUNT(*) AS days FROM "AMHC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ANDA' AS symbol, COUNT(*) AS days FROM "ANDA" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'APEX' AS symbol, COUNT(*) AS days FROM "APEX" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BCLI' AS symbol, COUNT(*) AS days FROM "BCLI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BHAT' AS symbol, COUNT(*) AS days FROM "BHAT" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BIOC' AS symbol, COUNT(*) AS days FROM "BIOC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BKYI' AS symbol, COUNT(*) AS days FROM "BKYI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BLFS' AS symbol, COUNT(*) AS days FROM "BLFS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BOSC' AS symbol, COUNT(*) AS days FROM "BOSC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BOTJ' AS symbol, COUNT(*) AS days FROM "BOTJ" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'BWEN' AS symbol, COUNT(*) AS days FROM "BWEN" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CBAT' AS symbol, COUNT(*) AS days FROM "CBAT" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CCCL' AS symbol, COUNT(*) AS days FROM "CCCL" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CDMOP' AS symbol, COUNT(*) AS days FROM "CDMOP" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CEMI' AS symbol, COUNT(*) AS days FROM "CEMI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CFBK' AS symbol, COUNT(*) AS days FROM "CFBK" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CFFA' AS symbol, COUNT(*) AS days FROM "CFFA" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CLRB' AS symbol, COUNT(*) AS days FROM "CLRB" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CORV' AS symbol, COUNT(*) AS days FROM "CORV" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CPAAU' AS symbol, COUNT(*) AS days FROM "CPAAU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CPAH' AS symbol, COUNT(*) AS days FROM "CPAH" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CUBA' AS symbol, COUNT(*) AS days FROM "CUBA" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'CVV' AS symbol, COUNT(*) AS days FROM "CVV" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'DZSI' AS symbol, COUNT(*) AS days FROM "DZSI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ELSE' AS symbol, COUNT(*) AS days FROM "ELSE" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'EXPC' AS symbol, COUNT(*) AS days FROM "EXPC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'EYEG' AS symbol, COUNT(*) AS days FROM "EYEG" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'FAMI' AS symbol, COUNT(*) AS days FROM "FAMI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'FNCB' AS symbol, COUNT(*) AS days FROM "FNCB" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'FSBW' AS symbol, COUNT(*) AS days FROM "FSBW" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'FTFT' AS symbol, COUNT(*) AS days FROM "FTFT" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'GDYN' AS symbol, COUNT(*) AS days FROM "GDYN" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'GLG' AS symbol, COUNT(*) AS days FROM "GLG" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'GRNVU' AS symbol, COUNT(*) AS days FROM "GRNVU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'GTEC' AS symbol, COUNT(*) AS days FROM "GTEC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'HCCOU' AS symbol, COUNT(*) AS days FROM "HCCOU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'HNNA' AS symbol, COUNT(*) AS days FROM "HNNA" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'HQI' AS symbol, COUNT(*) AS days FROM "HQI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'HRTX' AS symbol, COUNT(*) AS days FROM "HRTX" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'IDEX' AS symbol, COUNT(*) AS days FROM "IDEX" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'IGIC' AS symbol, COUNT(*) AS days FROM "IGIC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'IOTS' AS symbol, COUNT(*) AS days FROM "IOTS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ISNS' AS symbol, COUNT(*) AS days FROM "ISNS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ITI' AS symbol, COUNT(*) AS days FROM "ITI" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'LACQ' AS symbol, COUNT(*) AS days FROM "LACQ" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MBCN' AS symbol, COUNT(*) AS days FROM "MBCN" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MBNKP' AS symbol, COUNT(*) AS days FROM "MBNKP" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MCEP' AS symbol, COUNT(*) AS days FROM "MCEP" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MLND' AS symbol, COUNT(*) AS days FROM "MLND" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MMAC' AS symbol, COUNT(*) AS days FROM "MMAC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MNCLU' AS symbol, COUNT(*) AS days FROM "MNCLU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'MNPR' AS symbol, COUNT(*) AS days FROM "MNPR" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'NVEE' AS symbol, COUNT(*) AS days FROM "NVEE" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'NXTD' AS symbol, COUNT(*) AS days FROM "NXTD" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'OPOF' AS symbol, COUNT(*) AS days FROM "OPOF" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'OPTT' AS symbol, COUNT(*) AS days FROM "OPTT" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ORGO' AS symbol, COUNT(*) AS days FROM "ORGO" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'ORSNU' AS symbol, COUNT(*) AS days FROM "ORSNU" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'OTEL' AS symbol, COUNT(*) AS days FROM "OTEL" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PBFS' AS symbol, COUNT(*) AS days FROM "PBFS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PBTS' AS symbol, COUNT(*) AS days FROM "PBTS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PCSB' AS symbol, COUNT(*) AS days FROM "PCSB" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PECK' AS symbol, COUNT(*) AS days FROM "PECK" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PEIX' AS symbol, COUNT(*) AS days FROM "PEIX" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PFIE' AS symbol, COUNT(*) AS days FROM "PFIE" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'PLIN' AS symbol, COUNT(*) AS days FROM "PLIN" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'POPE' AS symbol, COUNT(*) AS days FROM "POPE" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'QRHC' AS symbol, COUNT(*) AS days FROM "QRHC" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'SES' AS symbol, COUNT(*) AS days FROM "SES" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'SHSP' AS symbol, COUNT(*) AS days FROM "SHSP" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'SNSS' AS symbol, COUNT(*) AS days FROM "SNSS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'SSNT' AS symbol, COUNT(*) AS days FROM "SSNT" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'STKS' AS symbol, COUNT(*) AS days FROM "STKS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'TGLS' AS symbol, COUNT(*) AS days FROM "TGLS" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'TMSR' AS symbol, COUNT(*) AS days FROM "TMSR" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'VERB' AS symbol, COUNT(*) AS days FROM "VERB" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'VMD' AS symbol, COUNT(*) AS days FROM "VMD" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'VRRM' AS symbol, COUNT(*) AS days FROM "VRRM" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'VTIQW' AS symbol, COUNT(*) AS days FROM "VTIQW" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'VVPR' AS symbol, COUNT(*) AS days FROM "VVPR" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'WHLM' AS symbol, COUNT(*) AS days FROM "WHLM" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'WHLR' AS symbol, COUNT(*) AS days FROM "WHLR" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'XBIOW' AS symbol, COUNT(*) AS days FROM "XBIOW" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
UNION ALL
SELECT 'XPEL' AS symbol, COUNT(*) AS days FROM "XPEL" WHERE "Date" >= '2019-01-01' AND "Date" <= '2019-12-31' AND "Low" > 0 AND ("High" - "Low") / "Low" > 0.20
) t ORDER BY days DESC, symbol ASC;
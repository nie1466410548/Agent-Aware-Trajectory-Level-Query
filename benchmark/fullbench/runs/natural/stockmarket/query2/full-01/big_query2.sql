SET max_expression_depth TO 100000;
SELECT Symbol, max_adj FROM (
SELECT 'AAAU' AS Symbol, MAX("Adj Close") AS max_adj FROM "AAAU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AADR' AS Symbol, MAX("Adj Close") AS max_adj FROM "AADR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ABEQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "ABEQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ACSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "ACSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ACWF' AS Symbol, MAX("Adj Close") AS max_adj FROM "ACWF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AFK' AS Symbol, MAX("Adj Close") AS max_adj FROM "AFK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AFLG' AS Symbol, MAX("Adj Close") AS max_adj FROM "AFLG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AFMC' AS Symbol, MAX("Adj Close") AS max_adj FROM "AFMC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AFSM' AS Symbol, MAX("Adj Close") AS max_adj FROM "AFSM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AFTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "AFTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AGG' AS Symbol, MAX("Adj Close") AS max_adj FROM "AGG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AGGP' AS Symbol, MAX("Adj Close") AS max_adj FROM "AGGP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AGGY' AS Symbol, MAX("Adj Close") AS max_adj FROM "AGGY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AGQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "AGQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AGZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "AGZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AIEQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "AIEQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AIIQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "AIIQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AMLP' AS Symbol, MAX("Adj Close") AS max_adj FROM "AMLP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AMOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "AMOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AMZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "AMZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AOA' AS Symbol, MAX("Adj Close") AS max_adj FROM "AOA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AOK' AS Symbol, MAX("Adj Close") AS max_adj FROM "AOK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "AOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "AOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ARGT' AS Symbol, MAX("Adj Close") AS max_adj FROM "ARGT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ARKF' AS Symbol, MAX("Adj Close") AS max_adj FROM "ARKF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ARKK' AS Symbol, MAX("Adj Close") AS max_adj FROM "ARKK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ARKW' AS Symbol, MAX("Adj Close") AS max_adj FROM "ARKW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ARMR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ARMR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ASEA' AS Symbol, MAX("Adj Close") AS max_adj FROM "ASEA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ASHR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ASHR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ASHS' AS Symbol, MAX("Adj Close") AS max_adj FROM "ASHS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ASHX' AS Symbol, MAX("Adj Close") AS max_adj FROM "ASHX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AUSF' AS Symbol, MAX("Adj Close") AS max_adj FROM "AUSF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AVDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "AVDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AVDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "AVDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AVEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "AVEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AVUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "AVUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AVUV' AS Symbol, MAX("Adj Close") AS max_adj FROM "AVUV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AWAY' AS Symbol, MAX("Adj Close") AS max_adj FROM "AWAY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AWTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "AWTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'AXJL' AS Symbol, MAX("Adj Close") AS max_adj FROM "AXJL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BAB' AS Symbol, MAX("Adj Close") AS max_adj FROM "BAB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BATT' AS Symbol, MAX("Adj Close") AS max_adj FROM "BATT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BBC' AS Symbol, MAX("Adj Close") AS max_adj FROM "BBC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BBP' AS Symbol, MAX("Adj Close") AS max_adj FROM "BBP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BCD' AS Symbol, MAX("Adj Close") AS max_adj FROM "BCD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BCI' AS Symbol, MAX("Adj Close") AS max_adj FROM "BCI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BDCY' AS Symbol, MAX("Adj Close") AS max_adj FROM "BDCY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BDRY' AS Symbol, MAX("Adj Close") AS max_adj FROM "BDRY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BFOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "BFOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BIBL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BIBL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "BIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BIZD' AS Symbol, MAX("Adj Close") AS max_adj FROM "BIZD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BKF' AS Symbol, MAX("Adj Close") AS max_adj FROM "BKF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BKLN' AS Symbol, MAX("Adj Close") AS max_adj FROM "BKLN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BLES' AS Symbol, MAX("Adj Close") AS max_adj FROM "BLES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BLHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "BLHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BLOK' AS Symbol, MAX("Adj Close") AS max_adj FROM "BLOK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "BLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BNDC' AS Symbol, MAX("Adj Close") AS max_adj FROM "BNDC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BNO' AS Symbol, MAX("Adj Close") AS max_adj FROM "BNO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BOIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BOIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BOND' AS Symbol, MAX("Adj Close") AS max_adj FROM "BOND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BOUT' AS Symbol, MAX("Adj Close") AS max_adj FROM "BOUT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BRF' AS Symbol, MAX("Adj Close") AS max_adj FROM "BRF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BRZU' AS Symbol, MAX("Adj Close") AS max_adj FROM "BRZU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BSV' AS Symbol, MAX("Adj Close") AS max_adj FROM "BSV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BTAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BTAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BUL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BUL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BUY' AS Symbol, MAX("Adj Close") AS max_adj FROM "BUY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BUYN' AS Symbol, MAX("Adj Close") AS max_adj FROM "BUYN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BVAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "BVAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "BWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BWZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "BWZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BYLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "BYLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'BZQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "BZQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CANE' AS Symbol, MAX("Adj Close") AS max_adj FROM "CANE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CBON' AS Symbol, MAX("Adj Close") AS max_adj FROM "CBON" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CCOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "CCOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "CEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CEW' AS Symbol, MAX("Adj Close") AS max_adj FROM "CEW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CGW' AS Symbol, MAX("Adj Close") AS max_adj FROM "CGW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHAD' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHAD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHAU' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHAU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHEP' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHEP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHGX' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHGX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIC' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIE' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIH' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHII' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHII" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIK' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIM' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIR' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIS' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIU' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CHIX' AS Symbol, MAX("Adj Close") AS max_adj FROM "CHIX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CLIX' AS Symbol, MAX("Adj Close") AS max_adj FROM "CLIX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CLTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "CLTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CMBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "CMBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CMDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "CMDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "CMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CN' AS Symbol, MAX("Adj Close") AS max_adj FROM "CN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CNBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "CNBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CNRG' AS Symbol, MAX("Adj Close") AS max_adj FROM "CNRG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CNXT' AS Symbol, MAX("Adj Close") AS max_adj FROM "CNXT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'COM' AS Symbol, MAX("Adj Close") AS max_adj FROM "COM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'COMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "COMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'COPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "COPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CORN' AS Symbol, MAX("Adj Close") AS max_adj FROM "CORN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CORP' AS Symbol, MAX("Adj Close") AS max_adj FROM "CORP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CPER' AS Symbol, MAX("Adj Close") AS max_adj FROM "CPER" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CPI' AS Symbol, MAX("Adj Close") AS max_adj FROM "CPI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CQQQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "CQQQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CRAK' AS Symbol, MAX("Adj Close") AS max_adj FROM "CRAK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CRBN' AS Symbol, MAX("Adj Close") AS max_adj FROM "CRBN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CROP' AS Symbol, MAX("Adj Close") AS max_adj FROM "CROP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CSD' AS Symbol, MAX("Adj Close") AS max_adj FROM "CSD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CURE' AS Symbol, MAX("Adj Close") AS max_adj FROM "CURE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CUT' AS Symbol, MAX("Adj Close") AS max_adj FROM "CUT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CVY' AS Symbol, MAX("Adj Close") AS max_adj FROM "CVY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CWB' AS Symbol, MAX("Adj Close") AS max_adj FROM "CWB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CWEB' AS Symbol, MAX("Adj Close") AS max_adj FROM "CWEB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CWI' AS Symbol, MAX("Adj Close") AS max_adj FROM "CWI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CWS' AS Symbol, MAX("Adj Close") AS max_adj FROM "CWS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CYB' AS Symbol, MAX("Adj Close") AS max_adj FROM "CYB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'CZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "CZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBA' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBAW' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBAW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBB' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBC' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBE' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBEH' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBEH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBEZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBEZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBGR' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBGR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBJP' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBJP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBO' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBP' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DBV' AS Symbol, MAX("Adj Close") AS max_adj FROM "DBV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DDG' AS Symbol, MAX("Adj Close") AS max_adj FROM "DDG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DEEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DEEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DES' AS Symbol, MAX("Adj Close") AS max_adj FROM "DES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DEUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DEUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DEW' AS Symbol, MAX("Adj Close") AS max_adj FROM "DEW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DFE' AS Symbol, MAX("Adj Close") AS max_adj FROM "DFE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DFEN' AS Symbol, MAX("Adj Close") AS max_adj FROM "DFEN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DFJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "DFJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DGL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DGL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DGRO' AS Symbol, MAX("Adj Close") AS max_adj FROM "DGRO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DGT' AS Symbol, MAX("Adj Close") AS max_adj FROM "DGT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DHS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DHS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIA' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIET' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIET" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIVA' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIVA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIVO' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIVO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DIVY' AS Symbol, MAX("Adj Close") AS max_adj FROM "DIVY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DJCB' AS Symbol, MAX("Adj Close") AS max_adj FROM "DJCB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DJD' AS Symbol, MAX("Adj Close") AS max_adj FROM "DJD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DLBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "DLBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DLN' AS Symbol, MAX("Adj Close") AS max_adj FROM "DLN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DLS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DLS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMRE' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMRE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMRI' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMRI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMRL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMRL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMRM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMRM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DMRS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DMRS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DNL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DNL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "DOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DOGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "DOGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DON' AS Symbol, MAX("Adj Close") AS max_adj FROM "DON" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "DOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DPST' AS Symbol, MAX("Adj Close") AS max_adj FROM "DPST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DRIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "DRIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DRN' AS Symbol, MAX("Adj Close") AS max_adj FROM "DRN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DRV' AS Symbol, MAX("Adj Close") AS max_adj FROM "DRV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DRW' AS Symbol, MAX("Adj Close") AS max_adj FROM "DRW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DSI' AS Symbol, MAX("Adj Close") AS max_adj FROM "DSI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DSTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DSTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DTD' AS Symbol, MAX("Adj Close") AS max_adj FROM "DTD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DTH' AS Symbol, MAX("Adj Close") AS max_adj FROM "DTH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DTN' AS Symbol, MAX("Adj Close") AS max_adj FROM "DTN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DUG' AS Symbol, MAX("Adj Close") AS max_adj FROM "DUG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DUSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "DUSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DUST' AS Symbol, MAX("Adj Close") AS max_adj FROM "DUST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DVP' AS Symbol, MAX("Adj Close") AS max_adj FROM "DVP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DVYA' AS Symbol, MAX("Adj Close") AS max_adj FROM "DVYA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DVYE' AS Symbol, MAX("Adj Close") AS max_adj FROM "DVYE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "DWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DWMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DWMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DWT' AS Symbol, MAX("Adj Close") AS max_adj FROM "DWT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "DWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DXD' AS Symbol, MAX("Adj Close") AS max_adj FROM "DXD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DXJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "DXJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DYNF' AS Symbol, MAX("Adj Close") AS max_adj FROM "DYNF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'DZK' AS Symbol, MAX("Adj Close") AS max_adj FROM "DZK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EAGG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EAGG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EASG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EASG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EASI' AS Symbol, MAX("Adj Close") AS max_adj FROM "EASI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EBND' AS Symbol, MAX("Adj Close") AS max_adj FROM "EBND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ECLN' AS Symbol, MAX("Adj Close") AS max_adj FROM "ECLN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ECNS' AS Symbol, MAX("Adj Close") AS max_adj FROM "ECNS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ECON' AS Symbol, MAX("Adj Close") AS max_adj FROM "ECON" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ECOZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "ECOZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDOW' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDOW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EDZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EDZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EELV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EELV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEMD' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEMD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEMS' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEMS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEMX' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEMX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EES' AS Symbol, MAX("Adj Close") AS max_adj FROM "EES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EET' AS Symbol, MAX("Adj Close") AS max_adj FROM "EET" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EEV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EEV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EFA' AS Symbol, MAX("Adj Close") AS max_adj FROM "EFA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EFAX' AS Symbol, MAX("Adj Close") AS max_adj FROM "EFAX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EFO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EFO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EFU' AS Symbol, MAX("Adj Close") AS max_adj FROM "EFU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EFZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EFZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EGPT' AS Symbol, MAX("Adj Close") AS max_adj FROM "EGPT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EIDO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EIDO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EINC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EINC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EIRL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EIRL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EIS' AS Symbol, MAX("Adj Close") AS max_adj FROM "EIS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EJAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "EJAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EJUL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EJUL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EKAR' AS Symbol, MAX("Adj Close") AS max_adj FROM "EKAR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ELD' AS Symbol, MAX("Adj Close") AS max_adj FROM "ELD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMAG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMAG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMBH' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMBH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMFM' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMFM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMLP' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMLP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMNT' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMNT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMQQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMQQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EMTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "EMTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ENFR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ENFR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ENTR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ENTR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPHE' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPHE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPI' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPP' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPS' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPU' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EPV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EPV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EQAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EQAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EQL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EQL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EQWL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EQWL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ERM' AS Symbol, MAX("Adj Close") AS max_adj FROM "ERM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ERSX' AS Symbol, MAX("Adj Close") AS max_adj FROM "ERSX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ERUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "ERUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ERX' AS Symbol, MAX("Adj Close") AS max_adj FROM "ERX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ERY' AS Symbol, MAX("Adj Close") AS max_adj FROM "ERY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ESGN' AS Symbol, MAX("Adj Close") AS max_adj FROM "ESGN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ESGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "ESGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ESNG' AS Symbol, MAX("Adj Close") AS max_adj FROM "ESNG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ETHO' AS Symbol, MAX("Adj Close") AS max_adj FROM "ETHO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUDG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUDG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUM' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUMV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUMV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EURL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EURL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EUSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EUSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EVX' AS Symbol, MAX("Adj Close") AS max_adj FROM "EVX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWA' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWCO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWCO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWD' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWG' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWH' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWI' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWK' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWL' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWMC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWMC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWN' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWO' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWP' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWRE' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWRE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWS' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWT' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWU' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWV' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWW' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWY' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EWZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EWZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "EXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "EZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EZJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "EZJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'EZM' AS Symbol, MAX("Adj Close") AS max_adj FROM "EZM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "FAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FAS' AS Symbol, MAX("Adj Close") AS max_adj FROM "FAS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FAUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "FAUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FAZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "FAZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FBND' AS Symbol, MAX("Adj Close") AS max_adj FROM "FBND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FBT' AS Symbol, MAX("Adj Close") AS max_adj FROM "FBT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FCG' AS Symbol, MAX("Adj Close") AS max_adj FROM "FCG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FCOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "FCOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FCOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FCOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDIS' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDIS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDLO' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDLO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDN' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDRR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDRR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FDVV' AS Symbol, MAX("Adj Close") AS max_adj FROM "FDVV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FENY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FENY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FEZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "FEZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FFIU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FFIU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FFR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FFR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FFTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FFTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FGD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FGD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FHLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "FHLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FIDI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FIDI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FIDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FIDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FILL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FILL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FISR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FISR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FITE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FITE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FIVA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FIVA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FIVG' AS Symbol, MAX("Adj Close") AS max_adj FROM "FIVG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FIW' AS Symbol, MAX("Adj Close") AS max_adj FROM "FIW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FJNK' AS Symbol, MAX("Adj Close") AS max_adj FROM "FJNK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLAG' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLAG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLAU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLAU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLAX' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLAX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLCA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLCA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLCB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLCB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLCH' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLCH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLCO' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLCO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLEE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLEE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLEH' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLEH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLFR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLFR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLGB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLGB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLGR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLGR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLHK' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLHK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLIY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLIY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLJH' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLJH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLJP' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLJP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLKR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLKR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLLA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLLA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLM' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLMI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLMI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLMX' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLMX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLQD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLQD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLQE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLQE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLQG' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLQG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLQH' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLQH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLRN' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLRN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLRT' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLRT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLRU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLRU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLSP' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLSP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLSW' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLSW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLTB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLTB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLTR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLTR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLTW' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLTW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLYT' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLYT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FLZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FLZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FM' AS Symbol, MAX("Adj Close") AS max_adj FROM "FM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FMAT' AS Symbol, MAX("Adj Close") AS max_adj FROM "FMAT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "FMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNCL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNCL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDC' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDF' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNDX' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNDX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FNI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FNI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FOVL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FOVL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FPE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FPE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FPEI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FPEI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "FPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FQAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FQAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FRAK' AS Symbol, MAX("Adj Close") AS max_adj FROM "FRAK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FREL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FREL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FRI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FRI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FSMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FSMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FSMD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FSMD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FSTA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FSTA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FTEC' AS Symbol, MAX("Adj Close") AS max_adj FROM "FTEC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FTLS' AS Symbol, MAX("Adj Close") AS max_adj FROM "FTLS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FTSD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FTSD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FUMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FUMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FUTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FUTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FVAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FVAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FVD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FVD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FVL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FVL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FWDB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FWDB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXA' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXB' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXC' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXD' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXE' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXG' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXH' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXL' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXN' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXO' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXP' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXR' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXU' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXY' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'FXZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "FXZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "GAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GAMR' AS Symbol, MAX("Adj Close") AS max_adj FROM "GAMR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GBDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "GBDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GBF' AS Symbol, MAX("Adj Close") AS max_adj FROM "GBF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GBIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "GBIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GBUG' AS Symbol, MAX("Adj Close") AS max_adj FROM "GBUG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GBUY' AS Symbol, MAX("Adj Close") AS max_adj FROM "GBUY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GCC' AS Symbol, MAX("Adj Close") AS max_adj FROM "GCC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GDAT' AS Symbol, MAX("Adj Close") AS max_adj FROM "GDAT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GDMA' AS Symbol, MAX("Adj Close") AS max_adj FROM "GDMA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GDNA' AS Symbol, MAX("Adj Close") AS max_adj FROM "GDNA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GDX' AS Symbol, MAX("Adj Close") AS max_adj FROM "GDX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GDXJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "GDXJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "GEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GFIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "GFIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GHYB' AS Symbol, MAX("Adj Close") AS max_adj FROM "GHYB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GIGB' AS Symbol, MAX("Adj Close") AS max_adj FROM "GIGB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GII' AS Symbol, MAX("Adj Close") AS max_adj FROM "GII" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLBY' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLBY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLIF' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLIF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLL' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GLTR' AS Symbol, MAX("Adj Close") AS max_adj FROM "GLTR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GMAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "GMAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "GMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GNR' AS Symbol, MAX("Adj Close") AS max_adj FROM "GNR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GOAU' AS Symbol, MAX("Adj Close") AS max_adj FROM "GOAU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GOEX' AS Symbol, MAX("Adj Close") AS max_adj FROM "GOEX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GQRE' AS Symbol, MAX("Adj Close") AS max_adj FROM "GQRE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GREK' AS Symbol, MAX("Adj Close") AS max_adj FROM "GREK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GRES' AS Symbol, MAX("Adj Close") AS max_adj FROM "GRES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GRNB' AS Symbol, MAX("Adj Close") AS max_adj FROM "GRNB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSIE' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSIE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSJY' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSJY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GSY' AS Symbol, MAX("Adj Close") AS max_adj FROM "GSY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GTO' AS Symbol, MAX("Adj Close") AS max_adj FROM "GTO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GUDB' AS Symbol, MAX("Adj Close") AS max_adj FROM "GUDB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GUNR' AS Symbol, MAX("Adj Close") AS max_adj FROM "GUNR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GURU' AS Symbol, MAX("Adj Close") AS max_adj FROM "GURU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GUSH' AS Symbol, MAX("Adj Close") AS max_adj FROM "GUSH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GVIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "GVIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "GWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GXC' AS Symbol, MAX("Adj Close") AS max_adj FROM "GXC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "GXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GXG' AS Symbol, MAX("Adj Close") AS max_adj FROM "GXG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'GYLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "GYLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HACK' AS Symbol, MAX("Adj Close") AS max_adj FROM "HACK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HAIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "HAIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HAP' AS Symbol, MAX("Adj Close") AS max_adj FROM "HAP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HAUD' AS Symbol, MAX("Adj Close") AS max_adj FROM "HAUD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HAUZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HAUZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HAWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "HAWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDAW' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDAW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDG' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDGE' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDGE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDMV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDMV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HECO' AS Symbol, MAX("Adj Close") AS max_adj FROM "HECO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEDJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEDJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWC' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWI' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWL' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWP' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWU' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWW' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEWY' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEWY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HEZU' AS Symbol, MAX("Adj Close") AS max_adj FROM "HEZU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HFXE' AS Symbol, MAX("Adj Close") AS max_adj FROM "HFXE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HFXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "HFXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HFXJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HFXJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HIBL' AS Symbol, MAX("Adj Close") AS max_adj FROM "HIBL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HIBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "HIBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HIPS' AS Symbol, MAX("Adj Close") AS max_adj FROM "HIPS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HJPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "HJPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HMOP' AS Symbol, MAX("Adj Close") AS max_adj FROM "HMOP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HOLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "HOLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HOMZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HOMZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HSCZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "HSCZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HSPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "HSPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HTAB' AS Symbol, MAX("Adj Close") AS max_adj FROM "HTAB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HTEC' AS Symbol, MAX("Adj Close") AS max_adj FROM "HTEC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HTRB' AS Symbol, MAX("Adj Close") AS max_adj FROM "HTRB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HTUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "HTUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HUSE' AS Symbol, MAX("Adj Close") AS max_adj FROM "HUSE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HUSV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HUSV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYDW' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYDW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYGH' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYGH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYGV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYGV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYS' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYTR' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYTR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'HYUP' AS Symbol, MAX("Adj Close") AS max_adj FROM "HYUP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IAI' AS Symbol, MAX("Adj Close") AS max_adj FROM "IAI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IAK' AS Symbol, MAX("Adj Close") AS max_adj FROM "IAK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IAT' AS Symbol, MAX("Adj Close") AS max_adj FROM "IAT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IAU' AS Symbol, MAX("Adj Close") AS max_adj FROM "IAU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBCE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBCE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBD' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDD' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDL' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDP' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDR' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDS' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDT' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBMI' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBMI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBMJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBMJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBMK' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBMK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IBND' AS Symbol, MAX("Adj Close") AS max_adj FROM "IBND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ICOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "ICOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDEV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDEV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDHQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDHQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDNA' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDNA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDRV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDRV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDX' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IEMG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IEMG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IEUR' AS Symbol, MAX("Adj Close") AS max_adj FROM "IEUR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IEV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IEV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IEZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IEZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IFLY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IFLY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IGBH' AS Symbol, MAX("Adj Close") AS max_adj FROM "IGBH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IGLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "IGLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IGM' AS Symbol, MAX("Adj Close") AS max_adj FROM "IGM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IGN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IGN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHAK' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHAK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHDG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHDG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHF' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHI' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IIGD' AS Symbol, MAX("Adj Close") AS max_adj FROM "IIGD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IIGV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IIGV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJH' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJK' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJR' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJS' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IJUL' AS Symbol, MAX("Adj Close") AS max_adj FROM "IJUL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ILF' AS Symbol, MAX("Adj Close") AS max_adj FROM "ILF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ILTB' AS Symbol, MAX("Adj Close") AS max_adj FROM "ILTB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IMTB' AS Symbol, MAX("Adj Close") AS max_adj FROM "IMTB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IMTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "IMTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'INCO' AS Symbol, MAX("Adj Close") AS max_adj FROM "INCO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'INDL' AS Symbol, MAX("Adj Close") AS max_adj FROM "INDL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'INDS' AS Symbol, MAX("Adj Close") AS max_adj FROM "INDS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'INKM' AS Symbol, MAX("Adj Close") AS max_adj FROM "INKM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'INTF' AS Symbol, MAX("Adj Close") AS max_adj FROM "INTF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IPAC' AS Symbol, MAX("Adj Close") AS max_adj FROM "IPAC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IPAY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IPAY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IPO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IPO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IPOS' AS Symbol, MAX("Adj Close") AS max_adj FROM "IPOS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQDF' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQDF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQLT' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQLT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQSI' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQSI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IQSU' AS Symbol, MAX("Adj Close") AS max_adj FROM "IQSU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IRBO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IRBO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ISCF' AS Symbol, MAX("Adj Close") AS max_adj FROM "ISCF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ISMD' AS Symbol, MAX("Adj Close") AS max_adj FROM "ISMD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ISRA' AS Symbol, MAX("Adj Close") AS max_adj FROM "ISRA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ISZE' AS Symbol, MAX("Adj Close") AS max_adj FROM "ISZE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ITEQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "ITEQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ITOT' AS Symbol, MAX("Adj Close") AS max_adj FROM "ITOT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVLU' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVLU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVOV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVOV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IVW' AS Symbol, MAX("Adj Close") AS max_adj FROM "IVW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWB' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWC' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWD' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWF' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWL' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWO' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWP' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWR' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWS' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWV' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IWY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IWY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXC' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXN' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXP' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IXSE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IXSE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYC' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYE' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYF' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYH' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYK' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYM' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYR' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYW' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'IYY' AS Symbol, MAX("Adj Close") AS max_adj FROM "IYY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JAGG' AS Symbol, MAX("Adj Close") AS max_adj FROM "JAGG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "JDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JDST' AS Symbol, MAX("Adj Close") AS max_adj FROM "JDST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JETS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JETS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHCS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHCS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMA' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMC' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMD' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHME' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHME" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMH' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMI' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHML' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHML" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMM' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMT' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHMU' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHMU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JHSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "JHSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JIGB' AS Symbol, MAX("Adj Close") AS max_adj FROM "JIGB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKD' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKE' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKF' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKG' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKH' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKK' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JKL' AS Symbol, MAX("Adj Close") AS max_adj FROM "JKL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JMBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JMBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JMIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "JMIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JMOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "JMOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JNK' AS Symbol, MAX("Adj Close") AS max_adj FROM "JNK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JNUG' AS Symbol, MAX("Adj Close") AS max_adj FROM "JNUG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JOYY' AS Symbol, MAX("Adj Close") AS max_adj FROM "JOYY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPED' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPED" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPGE' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPGE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPHF' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPHF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPLS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPLS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPME' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPME" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPMV' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPMV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPN' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPNL' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPNL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPSE' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPSE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JPXN' AS Symbol, MAX("Adj Close") AS max_adj FROM "JPXN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JQUA' AS Symbol, MAX("Adj Close") AS max_adj FROM "JQUA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JUST' AS Symbol, MAX("Adj Close") AS max_adj FROM "JUST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JVAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "JVAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'JXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "JXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KALL' AS Symbol, MAX("Adj Close") AS max_adj FROM "KALL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KARS' AS Symbol, MAX("Adj Close") AS max_adj FROM "KARS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KBA' AS Symbol, MAX("Adj Close") AS max_adj FROM "KBA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KBE' AS Symbol, MAX("Adj Close") AS max_adj FROM "KBE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KCCB' AS Symbol, MAX("Adj Close") AS max_adj FROM "KCCB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KCE' AS Symbol, MAX("Adj Close") AS max_adj FROM "KCE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KCNY' AS Symbol, MAX("Adj Close") AS max_adj FROM "KCNY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KDFI' AS Symbol, MAX("Adj Close") AS max_adj FROM "KDFI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KEMQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "KEMQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KEMX' AS Symbol, MAX("Adj Close") AS max_adj FROM "KEMX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KFYP' AS Symbol, MAX("Adj Close") AS max_adj FROM "KFYP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KGRN' AS Symbol, MAX("Adj Close") AS max_adj FROM "KGRN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KIE' AS Symbol, MAX("Adj Close") AS max_adj FROM "KIE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KLCD' AS Symbol, MAX("Adj Close") AS max_adj FROM "KLCD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KLDW' AS Symbol, MAX("Adj Close") AS max_adj FROM "KLDW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KMED' AS Symbol, MAX("Adj Close") AS max_adj FROM "KMED" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KNOW' AS Symbol, MAX("Adj Close") AS max_adj FROM "KNOW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KOIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "KOIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "KOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KOLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "KOLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KOMP' AS Symbol, MAX("Adj Close") AS max_adj FROM "KOMP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KORP' AS Symbol, MAX("Adj Close") AS max_adj FROM "KORP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KORU' AS Symbol, MAX("Adj Close") AS max_adj FROM "KORU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KRE' AS Symbol, MAX("Adj Close") AS max_adj FROM "KRE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "KSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KSCD' AS Symbol, MAX("Adj Close") AS max_adj FROM "KSCD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KURE' AS Symbol, MAX("Adj Close") AS max_adj FROM "KURE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KWEB' AS Symbol, MAX("Adj Close") AS max_adj FROM "KWEB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'KXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "KXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LABD' AS Symbol, MAX("Adj Close") AS max_adj FROM "LABD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LABU' AS Symbol, MAX("Adj Close") AS max_adj FROM "LABU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LACK' AS Symbol, MAX("Adj Close") AS max_adj FROM "LACK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LBJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "LBJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LCR' AS Symbol, MAX("Adj Close") AS max_adj FROM "LCR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LDRS' AS Symbol, MAX("Adj Close") AS max_adj FROM "LDRS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LDUR' AS Symbol, MAX("Adj Close") AS max_adj FROM "LDUR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LEMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "LEMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LEND' AS Symbol, MAX("Adj Close") AS max_adj FROM "LEND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LFEQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "LFEQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LGH' AS Symbol, MAX("Adj Close") AS max_adj FROM "LGH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LGLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "LGLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LGOV' AS Symbol, MAX("Adj Close") AS max_adj FROM "LGOV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LIT' AS Symbol, MAX("Adj Close") AS max_adj FROM "LIT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LMLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "LMLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LOUP' AS Symbol, MAX("Adj Close") AS max_adj FROM "LOUP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LOWC' AS Symbol, MAX("Adj Close") AS max_adj FROM "LOWC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LQD' AS Symbol, MAX("Adj Close") AS max_adj FROM "LQD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LQDH' AS Symbol, MAX("Adj Close") AS max_adj FROM "LQDH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LRGF' AS Symbol, MAX("Adj Close") AS max_adj FROM "LRGF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LRNZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "LRNZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LSAF' AS Symbol, MAX("Adj Close") AS max_adj FROM "LSAF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LSST' AS Symbol, MAX("Adj Close") AS max_adj FROM "LSST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "LTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'LTPZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "LTPZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MARB' AS Symbol, MAX("Adj Close") AS max_adj FROM "MARB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MCRO' AS Symbol, MAX("Adj Close") AS max_adj FROM "MCRO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "MDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MDYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "MDYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MDYV' AS Symbol, MAX("Adj Close") AS max_adj FROM "MDYV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MEXX' AS Symbol, MAX("Adj Close") AS max_adj FROM "MEXX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MFDX' AS Symbol, MAX("Adj Close") AS max_adj FROM "MFDX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MFEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "MFEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MFUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "MFUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MGC' AS Symbol, MAX("Adj Close") AS max_adj FROM "MGC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MGK' AS Symbol, MAX("Adj Close") AS max_adj FROM "MGK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MGV' AS Symbol, MAX("Adj Close") AS max_adj FROM "MGV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MIDF' AS Symbol, MAX("Adj Close") AS max_adj FROM "MIDF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MIDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "MIDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MINC' AS Symbol, MAX("Adj Close") AS max_adj FROM "MINC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MINT' AS Symbol, MAX("Adj Close") AS max_adj FROM "MINT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "MJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MJJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "MJJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MJO' AS Symbol, MAX("Adj Close") AS max_adj FROM "MJO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MLPA' AS Symbol, MAX("Adj Close") AS max_adj FROM "MLPA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MLPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "MLPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MLTI' AS Symbol, MAX("Adj Close") AS max_adj FROM "MLTI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MMIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "MMIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MMIT' AS Symbol, MAX("Adj Close") AS max_adj FROM "MMIT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MMTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "MMTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MNA' AS Symbol, MAX("Adj Close") AS max_adj FROM "MNA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "MOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "MOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MORT' AS Symbol, MAX("Adj Close") AS max_adj FROM "MORT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MOTO' AS Symbol, MAX("Adj Close") AS max_adj FROM "MOTO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MTGP' AS Symbol, MAX("Adj Close") AS max_adj FROM "MTGP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MUB' AS Symbol, MAX("Adj Close") AS max_adj FROM "MUB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MUNI' AS Symbol, MAX("Adj Close") AS max_adj FROM "MUNI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MUST' AS Symbol, MAX("Adj Close") AS max_adj FROM "MUST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MUTE' AS Symbol, MAX("Adj Close") AS max_adj FROM "MUTE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MVIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "MVIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MVV' AS Symbol, MAX("Adj Close") AS max_adj FROM "MVV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MXDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "MXDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MXDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "MXDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "MXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MYY' AS Symbol, MAX("Adj Close") AS max_adj FROM "MYY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'MZZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "MZZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NACP' AS Symbol, MAX("Adj Close") AS max_adj FROM "NACP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NAIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "NAIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NANR' AS Symbol, MAX("Adj Close") AS max_adj FROM "NANR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NEED' AS Symbol, MAX("Adj Close") AS max_adj FROM "NEED" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NERD' AS Symbol, MAX("Adj Close") AS max_adj FROM "NERD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NETL' AS Symbol, MAX("Adj Close") AS max_adj FROM "NETL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NFLT' AS Symbol, MAX("Adj Close") AS max_adj FROM "NFLT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NFRA' AS Symbol, MAX("Adj Close") AS max_adj FROM "NFRA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NGE' AS Symbol, MAX("Adj Close") AS max_adj FROM "NGE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NLR' AS Symbol, MAX("Adj Close") AS max_adj FROM "NLR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NORW' AS Symbol, MAX("Adj Close") AS max_adj FROM "NORW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NTSX' AS Symbol, MAX("Adj Close") AS max_adj FROM "NTSX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUAG' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUAG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUBD' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUBD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUGT' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUGT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NUSI' AS Symbol, MAX("Adj Close") AS max_adj FROM "NUSI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'NYF' AS Symbol, MAX("Adj Close") AS max_adj FROM "NYF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OBOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "OBOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OCIO' AS Symbol, MAX("Adj Close") AS max_adj FROM "OCIO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "OEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OEUR' AS Symbol, MAX("Adj Close") AS max_adj FROM "OEUR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OGIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "OGIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OIH' AS Symbol, MAX("Adj Close") AS max_adj FROM "OIH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "OIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ONEO' AS Symbol, MAX("Adj Close") AS max_adj FROM "ONEO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ONEV' AS Symbol, MAX("Adj Close") AS max_adj FROM "ONEV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ONEY' AS Symbol, MAX("Adj Close") AS max_adj FROM "ONEY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ONLN' AS Symbol, MAX("Adj Close") AS max_adj FROM "ONLN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OPER' AS Symbol, MAX("Adj Close") AS max_adj FROM "OPER" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OSCV' AS Symbol, MAX("Adj Close") AS max_adj FROM "OSCV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OUNZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "OUNZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OUSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "OUSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OUSM' AS Symbol, MAX("Adj Close") AS max_adj FROM "OUSM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OVB' AS Symbol, MAX("Adj Close") AS max_adj FROM "OVB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OVF' AS Symbol, MAX("Adj Close") AS max_adj FROM "OVF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OVL' AS Symbol, MAX("Adj Close") AS max_adj FROM "OVL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "OVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'OVS' AS Symbol, MAX("Adj Close") AS max_adj FROM "OVS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PACA' AS Symbol, MAX("Adj Close") AS max_adj FROM "PACA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PAK' AS Symbol, MAX("Adj Close") AS max_adj FROM "PAK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PALL' AS Symbol, MAX("Adj Close") AS max_adj FROM "PALL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PASS' AS Symbol, MAX("Adj Close") AS max_adj FROM "PASS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBD' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBE' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBP' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PBW' AS Symbol, MAX("Adj Close") AS max_adj FROM "PBW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PCEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "PCEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PCY' AS Symbol, MAX("Adj Close") AS max_adj FROM "PCY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PDN' AS Symbol, MAX("Adj Close") AS max_adj FROM "PDN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PEJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PEJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PEK' AS Symbol, MAX("Adj Close") AS max_adj FROM "PEK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PEXL' AS Symbol, MAX("Adj Close") AS max_adj FROM "PEXL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFFA' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFFA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFFD' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFFD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFFR' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFFR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PFXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "PFXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PGAL' AS Symbol, MAX("Adj Close") AS max_adj FROM "PGAL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PGF' AS Symbol, MAX("Adj Close") AS max_adj FROM "PGF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PGHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "PGHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PGX' AS Symbol, MAX("Adj Close") AS max_adj FROM "PGX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PHB' AS Symbol, MAX("Adj Close") AS max_adj FROM "PHB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PHDG' AS Symbol, MAX("Adj Close") AS max_adj FROM "PHDG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PHYL' AS Symbol, MAX("Adj Close") AS max_adj FROM "PHYL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PHYS' AS Symbol, MAX("Adj Close") AS max_adj FROM "PHYS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PICB' AS Symbol, MAX("Adj Close") AS max_adj FROM "PICB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PILL' AS Symbol, MAX("Adj Close") AS max_adj FROM "PILL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "PIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PJP' AS Symbol, MAX("Adj Close") AS max_adj FROM "PJP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PKB' AS Symbol, MAX("Adj Close") AS max_adj FROM "PKB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PLAT' AS Symbol, MAX("Adj Close") AS max_adj FROM "PLAT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PLTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "PLTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPA' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPLT' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPLT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPMC' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPMC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PPTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "PPTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PQIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "PQIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PQLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "PQLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PQSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "PQSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PQSV' AS Symbol, MAX("Adj Close") AS max_adj FROM "PQSV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PRF' AS Symbol, MAX("Adj Close") AS max_adj FROM "PRF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSI' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSK' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSP' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PSR' AS Symbol, MAX("Adj Close") AS max_adj FROM "PSR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PST' AS Symbol, MAX("Adj Close") AS max_adj FROM "PST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PTBD' AS Symbol, MAX("Adj Close") AS max_adj FROM "PTBD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PTIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "PTIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PULS' AS Symbol, MAX("Adj Close") AS max_adj FROM "PULS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PUTW' AS Symbol, MAX("Adj Close") AS max_adj FROM "PUTW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PVI' AS Symbol, MAX("Adj Close") AS max_adj FROM "PVI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PWB' AS Symbol, MAX("Adj Close") AS max_adj FROM "PWB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PWC' AS Symbol, MAX("Adj Close") AS max_adj FROM "PWC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PWV' AS Symbol, MAX("Adj Close") AS max_adj FROM "PWV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PWZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PWZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PXE' AS Symbol, MAX("Adj Close") AS max_adj FROM "PXE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "PXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PXH' AS Symbol, MAX("Adj Close") AS max_adj FROM "PXH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PXJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PXJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PXQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "PXQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "PZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PZD' AS Symbol, MAX("Adj Close") AS max_adj FROM "PZD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'PZT' AS Symbol, MAX("Adj Close") AS max_adj FROM "PZT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QAI' AS Symbol, MAX("Adj Close") AS max_adj FROM "QAI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QARP' AS Symbol, MAX("Adj Close") AS max_adj FROM "QARP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QDEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "QDEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QDF' AS Symbol, MAX("Adj Close") AS max_adj FROM "QDF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "QDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QDYN' AS Symbol, MAX("Adj Close") AS max_adj FROM "QDYN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QED' AS Symbol, MAX("Adj Close") AS max_adj FROM "QED" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QEFA' AS Symbol, MAX("Adj Close") AS max_adj FROM "QEFA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QEMM' AS Symbol, MAX("Adj Close") AS max_adj FROM "QEMM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QGRO' AS Symbol, MAX("Adj Close") AS max_adj FROM "QGRO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QGTA' AS Symbol, MAX("Adj Close") AS max_adj FROM "QGTA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QID' AS Symbol, MAX("Adj Close") AS max_adj FROM "QID" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QINT' AS Symbol, MAX("Adj Close") AS max_adj FROM "QINT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLS' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLTA' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLTA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLVD' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLVD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QLVE' AS Symbol, MAX("Adj Close") AS max_adj FROM "QLVE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QMJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "QMJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QMN' AS Symbol, MAX("Adj Close") AS max_adj FROM "QMN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QQH' AS Symbol, MAX("Adj Close") AS max_adj FROM "QQH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QQQE' AS Symbol, MAX("Adj Close") AS max_adj FROM "QQQE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QRFT' AS Symbol, MAX("Adj Close") AS max_adj FROM "QRFT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QSY' AS Symbol, MAX("Adj Close") AS max_adj FROM "QSY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QTUM' AS Symbol, MAX("Adj Close") AS max_adj FROM "QTUM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "QUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "QVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'QWLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "QWLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RAAX' AS Symbol, MAX("Adj Close") AS max_adj FROM "RAAX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RAFE' AS Symbol, MAX("Adj Close") AS max_adj FROM "RAFE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RALS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RALS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RAVI' AS Symbol, MAX("Adj Close") AS max_adj FROM "RAVI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RBIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "RBIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RBUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RBUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RCD' AS Symbol, MAX("Adj Close") AS max_adj FROM "RCD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "RDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RDOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "RDOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RECS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RECS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REET' AS Symbol, MAX("Adj Close") AS max_adj FROM "REET" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REK' AS Symbol, MAX("Adj Close") AS max_adj FROM "REK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REMX' AS Symbol, MAX("Adj Close") AS max_adj FROM "REMX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RETL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RETL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REVS' AS Symbol, MAX("Adj Close") AS max_adj FROM "REVS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REW' AS Symbol, MAX("Adj Close") AS max_adj FROM "REW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'REZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "REZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFCI' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFCI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFDA' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFDA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFFC' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFFC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFG' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFUN' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFUN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RFV' AS Symbol, MAX("Adj Close") AS max_adj FROM "RFV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RGI' AS Symbol, MAX("Adj Close") AS max_adj FROM "RGI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RHS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RHS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RIGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RIGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RINF' AS Symbol, MAX("Adj Close") AS max_adj FROM "RINF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RISE' AS Symbol, MAX("Adj Close") AS max_adj FROM "RISE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RLY' AS Symbol, MAX("Adj Close") AS max_adj FROM "RLY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROAM' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROAM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROBO' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROBO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RODM' AS Symbol, MAX("Adj Close") AS max_adj FROM "RODM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROKT' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROKT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROM' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROOF' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROOF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RORE' AS Symbol, MAX("Adj Close") AS max_adj FROM "RORE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ROUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "ROUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RPAR' AS Symbol, MAX("Adj Close") AS max_adj FROM "RPAR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RPG' AS Symbol, MAX("Adj Close") AS max_adj FROM "RPG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RPV' AS Symbol, MAX("Adj Close") AS max_adj FROM "RPV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RSP' AS Symbol, MAX("Adj Close") AS max_adj FROM "RSP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "RTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RUSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RUSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RVNU' AS Symbol, MAX("Adj Close") AS max_adj FROM "RVNU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWCD' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWCD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWDC' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWDC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWED' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWED" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWGV' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWGV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWIU' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWIU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWK' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWLS' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWLS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWO' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWR' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWUI' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWUI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWVG' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWVG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RWX' AS Symbol, MAX("Adj Close") AS max_adj FROM "RWX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RXD' AS Symbol, MAX("Adj Close") AS max_adj FROM "RXD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "RXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RXL' AS Symbol, MAX("Adj Close") AS max_adj FROM "RXL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYE' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYF' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYH' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYT' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYU' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RYZZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "RYZZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RZG' AS Symbol, MAX("Adj Close") AS max_adj FROM "RZG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'RZV' AS Symbol, MAX("Adj Close") AS max_adj FROM "RZV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SAA' AS Symbol, MAX("Adj Close") AS max_adj FROM "SAA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SBB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SBB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SBIO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SBIO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SBM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SBM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCAP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCAP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCC' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHA' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHC' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHH' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHI' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHK' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHR' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCHZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCHZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCID' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCID" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCIF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCIF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCIJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCIJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCIU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCIU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCIX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCIX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SCO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SCO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDAG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDAG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDCI' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDCI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDGA' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDGA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDOW' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDOW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SEF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SEF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SEIX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SEIX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SFY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SFY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SFYF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SFYF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SFYX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SFYX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SGDJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SGDJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SGDM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SGDM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SGOL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SGOL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SH' AS Symbol, MAX("Adj Close") AS max_adj FROM "SH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SHE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SHE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SHM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SHM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SHYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SHYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SHYL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SHYL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SIJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SIJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SILJ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SILJ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SIMS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SIMS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SIVR' AS Symbol, MAX("Adj Close") AS max_adj FROM "SIVR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SIZE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SIZE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SJB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SJB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SJNK' AS Symbol, MAX("Adj Close") AS max_adj FROM "SJNK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SKF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SKF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SLX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SLX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SLY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SLY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SLYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SLYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SLYV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SLYV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMDD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMDD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMEZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMEZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMLF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMLF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMLL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMLL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMMU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMMU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMN' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SMOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SMOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SNPE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SNPE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SOIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SOIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SOXL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SOXL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SOXS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SOXS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SOYB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SOYB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPAB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPAB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPBO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPBO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPDN' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPDN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPDV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPDV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPDW' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPDW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPFF' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPFF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPGM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPGM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPGP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPGP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPHB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPHB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPHD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPHD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPHQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPHQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPHY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPHY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPIB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPIB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPLG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPLG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPMB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPMB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPMD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPMD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPPP' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPPP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPSB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPSB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPSK' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPSK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPSM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPSM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPTI' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPTI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPTM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPTM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPTS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPTS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPUU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPUU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPVU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPVU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXL' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXN' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXT' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXU' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPXV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPXV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPYB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPYB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPYD' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPYD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPYV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPYV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SPYX' AS Symbol, MAX("Adj Close") AS max_adj FROM "SPYX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SRLN' AS Symbol, MAX("Adj Close") AS max_adj FROM "SRLN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SRS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SRS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SRTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SRTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SRVR' AS Symbol, MAX("Adj Close") AS max_adj FROM "SRVR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SSO' AS Symbol, MAX("Adj Close") AS max_adj FROM "SSO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SSPY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SSPY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SSUS' AS Symbol, MAX("Adj Close") AS max_adj FROM "SSUS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'STIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "STIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'STPZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "STPZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SUB' AS Symbol, MAX("Adj Close") AS max_adj FROM "SUB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SUSA' AS Symbol, MAX("Adj Close") AS max_adj FROM "SUSA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SVXY' AS Symbol, MAX("Adj Close") AS max_adj FROM "SVXY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SWAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "SWAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SYE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SYE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "SYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SYV' AS Symbol, MAX("Adj Close") AS max_adj FROM "SYV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SZK' AS Symbol, MAX("Adj Close") AS max_adj FROM "SZK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'SZNE' AS Symbol, MAX("Adj Close") AS max_adj FROM "SZNE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TAGS' AS Symbol, MAX("Adj Close") AS max_adj FROM "TAGS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "TAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TAWK' AS Symbol, MAX("Adj Close") AS max_adj FROM "TAWK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TAXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "TAXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TBF' AS Symbol, MAX("Adj Close") AS max_adj FROM "TBF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TBND' AS Symbol, MAX("Adj Close") AS max_adj FROM "TBND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TBT' AS Symbol, MAX("Adj Close") AS max_adj FROM "TBT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TBX' AS Symbol, MAX("Adj Close") AS max_adj FROM "TBX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TDTF' AS Symbol, MAX("Adj Close") AS max_adj FROM "TDTF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TDTT' AS Symbol, MAX("Adj Close") AS max_adj FROM "TDTT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TECB' AS Symbol, MAX("Adj Close") AS max_adj FROM "TECB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TECL' AS Symbol, MAX("Adj Close") AS max_adj FROM "TECL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TECS' AS Symbol, MAX("Adj Close") AS max_adj FROM "TECS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TERM' AS Symbol, MAX("Adj Close") AS max_adj FROM "TERM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TFI' AS Symbol, MAX("Adj Close") AS max_adj FROM "TFI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TFLO' AS Symbol, MAX("Adj Close") AS max_adj FROM "TFLO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'THCX' AS Symbol, MAX("Adj Close") AS max_adj FROM "THCX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'THD' AS Symbol, MAX("Adj Close") AS max_adj FROM "THD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "TIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TIPX' AS Symbol, MAX("Adj Close") AS max_adj FROM "TIPX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TIPZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "TIPZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TLDH' AS Symbol, MAX("Adj Close") AS max_adj FROM "TLDH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TLEH' AS Symbol, MAX("Adj Close") AS max_adj FROM "TLEH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TLH' AS Symbol, MAX("Adj Close") AS max_adj FROM "TLH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TLTD' AS Symbol, MAX("Adj Close") AS max_adj FROM "TLTD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TLTE' AS Symbol, MAX("Adj Close") AS max_adj FROM "TLTE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "TMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TMV' AS Symbol, MAX("Adj Close") AS max_adj FROM "TMV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TNA' AS Symbol, MAX("Adj Close") AS max_adj FROM "TNA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TOK' AS Symbol, MAX("Adj Close") AS max_adj FROM "TOK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TOLZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "TOLZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TOTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "TOTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPHD' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPHD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPIF' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPIF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPOR' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPOR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPSC' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPSC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TPYP' AS Symbol, MAX("Adj Close") AS max_adj FROM "TPYP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TRND' AS Symbol, MAX("Adj Close") AS max_adj FROM "TRND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TTT' AS Symbol, MAX("Adj Close") AS max_adj FROM "TTT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "TWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TYBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "TYBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TYD' AS Symbol, MAX("Adj Close") AS max_adj FROM "TYD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TYO' AS Symbol, MAX("Adj Close") AS max_adj FROM "TYO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'TZA' AS Symbol, MAX("Adj Close") AS max_adj FROM "TZA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UBOT' AS Symbol, MAX("Adj Close") AS max_adj FROM "UBOT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "UBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UBT' AS Symbol, MAX("Adj Close") AS max_adj FROM "UBT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UCC' AS Symbol, MAX("Adj Close") AS max_adj FROM "UCC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UCO' AS Symbol, MAX("Adj Close") AS max_adj FROM "UCO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UCON' AS Symbol, MAX("Adj Close") AS max_adj FROM "UCON" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UDN' AS Symbol, MAX("Adj Close") AS max_adj FROM "UDN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UDOW' AS Symbol, MAX("Adj Close") AS max_adj FROM "UDOW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UEVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "UEVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UGA' AS Symbol, MAX("Adj Close") AS max_adj FROM "UGA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UGE' AS Symbol, MAX("Adj Close") AS max_adj FROM "UGE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UGL' AS Symbol, MAX("Adj Close") AS max_adj FROM "UGL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UITB' AS Symbol, MAX("Adj Close") AS max_adj FROM "UITB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UIVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "UIVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UJB' AS Symbol, MAX("Adj Close") AS max_adj FROM "UJB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ULBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ULBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ULE' AS Symbol, MAX("Adj Close") AS max_adj FROM "ULE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ULST' AS Symbol, MAX("Adj Close") AS max_adj FROM "ULST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ULTR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ULTR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ULVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "ULVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UMDD' AS Symbol, MAX("Adj Close") AS max_adj FROM "UMDD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UNG' AS Symbol, MAX("Adj Close") AS max_adj FROM "UNG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UNL' AS Symbol, MAX("Adj Close") AS max_adj FROM "UNL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UPRO' AS Symbol, MAX("Adj Close") AS max_adj FROM "UPRO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UPV' AS Symbol, MAX("Adj Close") AS max_adj FROM "UPV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UPW' AS Symbol, MAX("Adj Close") AS max_adj FROM "UPW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'URA' AS Symbol, MAX("Adj Close") AS max_adj FROM "URA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'URE' AS Symbol, MAX("Adj Close") AS max_adj FROM "URE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'URNM' AS Symbol, MAX("Adj Close") AS max_adj FROM "URNM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'URTH' AS Symbol, MAX("Adj Close") AS max_adj FROM "URTH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'URTY' AS Symbol, MAX("Adj Close") AS max_adj FROM "URTY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USAI' AS Symbol, MAX("Adj Close") AS max_adj FROM "USAI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USCI' AS Symbol, MAX("Adj Close") AS max_adj FROM "USCI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USD' AS Symbol, MAX("Adj Close") AS max_adj FROM "USD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USDU' AS Symbol, MAX("Adj Close") AS max_adj FROM "USDU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USDY' AS Symbol, MAX("Adj Close") AS max_adj FROM "USDY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USFR' AS Symbol, MAX("Adj Close") AS max_adj FROM "USFR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USHG' AS Symbol, MAX("Adj Close") AS max_adj FROM "USHG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USI' AS Symbol, MAX("Adj Close") AS max_adj FROM "USI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USL' AS Symbol, MAX("Adj Close") AS max_adj FROM "USL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USO' AS Symbol, MAX("Adj Close") AS max_adj FROM "USO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USRT' AS Symbol, MAX("Adj Close") AS max_adj FROM "USRT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USSG' AS Symbol, MAX("Adj Close") AS max_adj FROM "USSG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UST' AS Symbol, MAX("Adj Close") AS max_adj FROM "UST" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USTB' AS Symbol, MAX("Adj Close") AS max_adj FROM "USTB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'USVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "USVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UTES' AS Symbol, MAX("Adj Close") AS max_adj FROM "UTES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UTRN' AS Symbol, MAX("Adj Close") AS max_adj FROM "UTRN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UTSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "UTSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UUP' AS Symbol, MAX("Adj Close") AS max_adj FROM "UUP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UVXY' AS Symbol, MAX("Adj Close") AS max_adj FROM "UVXY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UWM' AS Symbol, MAX("Adj Close") AS max_adj FROM "UWM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UWT' AS Symbol, MAX("Adj Close") AS max_adj FROM "UWT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "UXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UYG' AS Symbol, MAX("Adj Close") AS max_adj FROM "UYG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'UYM' AS Symbol, MAX("Adj Close") AS max_adj FROM "UYM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VALQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "VALQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VALT' AS Symbol, MAX("Adj Close") AS max_adj FROM "VALT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VAW' AS Symbol, MAX("Adj Close") AS max_adj FROM "VAW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VB' AS Symbol, MAX("Adj Close") AS max_adj FROM "VB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VBK' AS Symbol, MAX("Adj Close") AS max_adj FROM "VBK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VBND' AS Symbol, MAX("Adj Close") AS max_adj FROM "VBND" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "VBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VCR' AS Symbol, MAX("Adj Close") AS max_adj FROM "VCR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VDC' AS Symbol, MAX("Adj Close") AS max_adj FROM "VDC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VDE' AS Symbol, MAX("Adj Close") AS max_adj FROM "VDE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VEA' AS Symbol, MAX("Adj Close") AS max_adj FROM "VEA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VEGA' AS Symbol, MAX("Adj Close") AS max_adj FROM "VEGA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VEGI' AS Symbol, MAX("Adj Close") AS max_adj FROM "VEGI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VEGN' AS Symbol, MAX("Adj Close") AS max_adj FROM "VEGN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "VEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VFH' AS Symbol, MAX("Adj Close") AS max_adj FROM "VFH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VGFO' AS Symbol, MAX("Adj Close") AS max_adj FROM "VGFO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VGK' AS Symbol, MAX("Adj Close") AS max_adj FROM "VGK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VGT' AS Symbol, MAX("Adj Close") AS max_adj FROM "VGT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VHT' AS Symbol, MAX("Adj Close") AS max_adj FROM "VHT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIDI' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIDI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIOV' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIOV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIS' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIXM' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIXM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VIXY' AS Symbol, MAX("Adj Close") AS max_adj FROM "VIXY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VLU' AS Symbol, MAX("Adj Close") AS max_adj FROM "VLU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VNLA' AS Symbol, MAX("Adj Close") AS max_adj FROM "VNLA" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VNQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "VNQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VO' AS Symbol, MAX("Adj Close") AS max_adj FROM "VO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOE' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOO' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOOG' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOOG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOOV' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOOV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOT' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VOX' AS Symbol, MAX("Adj Close") AS max_adj FROM "VOX" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VPC' AS Symbol, MAX("Adj Close") AS max_adj FROM "VPC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VPL' AS Symbol, MAX("Adj Close") AS max_adj FROM "VPL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VPU' AS Symbol, MAX("Adj Close") AS max_adj FROM "VPU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VRAI' AS Symbol, MAX("Adj Close") AS max_adj FROM "VRAI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VRP' AS Symbol, MAX("Adj Close") AS max_adj FROM "VRP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "VSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VSS' AS Symbol, MAX("Adj Close") AS max_adj FROM "VSS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VT' AS Symbol, MAX("Adj Close") AS max_adj FROM "VT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VTEB' AS Symbol, MAX("Adj Close") AS max_adj FROM "VTEB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VTI' AS Symbol, MAX("Adj Close") AS max_adj FROM "VTI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VTV' AS Symbol, MAX("Adj Close") AS max_adj FROM "VTV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VUG' AS Symbol, MAX("Adj Close") AS max_adj FROM "VUG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VUSE' AS Symbol, MAX("Adj Close") AS max_adj FROM "VUSE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VV' AS Symbol, MAX("Adj Close") AS max_adj FROM "VV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VWO' AS Symbol, MAX("Adj Close") AS max_adj FROM "VWO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VXF' AS Symbol, MAX("Adj Close") AS max_adj FROM "VXF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'VYM' AS Symbol, MAX("Adj Close") AS max_adj FROM "VYM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WANT' AS Symbol, MAX("Adj Close") AS max_adj FROM "WANT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIE' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIF' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBII' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBII" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIL' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIN' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIT' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WBIY' AS Symbol, MAX("Adj Close") AS max_adj FROM "WBIY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WCHN' AS Symbol, MAX("Adj Close") AS max_adj FROM "WCHN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "WDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WEAT' AS Symbol, MAX("Adj Close") AS max_adj FROM "WEAT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WEBL' AS Symbol, MAX("Adj Close") AS max_adj FROM "WEBL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WEBS' AS Symbol, MAX("Adj Close") AS max_adj FROM "WEBS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WIP' AS Symbol, MAX("Adj Close") AS max_adj FROM "WIP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WIZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "WIZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WOMN' AS Symbol, MAX("Adj Close") AS max_adj FROM "WOMN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WPS' AS Symbol, MAX("Adj Close") AS max_adj FROM "WPS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WTMF' AS Symbol, MAX("Adj Close") AS max_adj FROM "WTMF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'WWJD' AS Symbol, MAX("Adj Close") AS max_adj FROM "WWJD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XAR' AS Symbol, MAX("Adj Close") AS max_adj FROM "XAR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XBI' AS Symbol, MAX("Adj Close") AS max_adj FROM "XBI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XBUY' AS Symbol, MAX("Adj Close") AS max_adj FROM "XBUY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XCEM' AS Symbol, MAX("Adj Close") AS max_adj FROM "XCEM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XCOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "XCOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XDIV' AS Symbol, MAX("Adj Close") AS max_adj FROM "XDIV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XES' AS Symbol, MAX("Adj Close") AS max_adj FROM "XES" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XHB' AS Symbol, MAX("Adj Close") AS max_adj FROM "XHB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XHE' AS Symbol, MAX("Adj Close") AS max_adj FROM "XHE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XHS' AS Symbol, MAX("Adj Close") AS max_adj FROM "XHS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XITK' AS Symbol, MAX("Adj Close") AS max_adj FROM "XITK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLB' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLC' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLC" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLE' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLF' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLF" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLG' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLI' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLK' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLP' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLRE' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLRE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLSR' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLSR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLU' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XLY' AS Symbol, MAX("Adj Close") AS max_adj FROM "XLY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XME' AS Symbol, MAX("Adj Close") AS max_adj FROM "XME" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XMHQ' AS Symbol, MAX("Adj Close") AS max_adj FROM "XMHQ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XMLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "XMLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XMMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "XMMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XMVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "XMVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XNTK' AS Symbol, MAX("Adj Close") AS max_adj FROM "XNTK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XOP' AS Symbol, MAX("Adj Close") AS max_adj FROM "XOP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XOUT' AS Symbol, MAX("Adj Close") AS max_adj FROM "XOUT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XPH' AS Symbol, MAX("Adj Close") AS max_adj FROM "XPH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XPP' AS Symbol, MAX("Adj Close") AS max_adj FROM "XPP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XRLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "XRLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XRT' AS Symbol, MAX("Adj Close") AS max_adj FROM "XRT" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSD' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSLV' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSLV" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSMO' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSMO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSOE' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSOE" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSVM' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSVM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XSW' AS Symbol, MAX("Adj Close") AS max_adj FROM "XSW" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XTH' AS Symbol, MAX("Adj Close") AS max_adj FROM "XTH" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XTL' AS Symbol, MAX("Adj Close") AS max_adj FROM "XTL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XTN' AS Symbol, MAX("Adj Close") AS max_adj FROM "XTN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'XWEB' AS Symbol, MAX("Adj Close") AS max_adj FROM "XWEB" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YANG' AS Symbol, MAX("Adj Close") AS max_adj FROM "YANG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YCL' AS Symbol, MAX("Adj Close") AS max_adj FROM "YCL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YCOM' AS Symbol, MAX("Adj Close") AS max_adj FROM "YCOM" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YCS' AS Symbol, MAX("Adj Close") AS max_adj FROM "YCS" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YINN' AS Symbol, MAX("Adj Close") AS max_adj FROM "YINN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YLD' AS Symbol, MAX("Adj Close") AS max_adj FROM "YLD" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YOLO' AS Symbol, MAX("Adj Close") AS max_adj FROM "YOLO" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YXI' AS Symbol, MAX("Adj Close") AS max_adj FROM "YXI" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'YYY' AS Symbol, MAX("Adj Close") AS max_adj FROM "YYY" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZCAN' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZCAN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZDEU' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZDEU" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZGBR' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZGBR" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZHOK' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZHOK" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZIG' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZIG" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZJPN' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZJPN" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZMLP' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZMLP" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZROZ' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZROZ" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
UNION ALL
SELECT 'ZSL' AS Symbol, MAX("Adj Close") AS max_adj FROM "ZSL" WHERE "Date" >= '2015-01-01' AND "Date" <= '2015-12-31'
) t WHERE max_adj > 200 ORDER BY Symbol
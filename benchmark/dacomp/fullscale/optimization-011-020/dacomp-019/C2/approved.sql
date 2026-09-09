-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_019_c2" AS
SELECT "Origin / Tier (Domestic/Imported/JV)" AS __g0, "GSP Certification Status" AS __g1, "Storage conditions (room temperature/cool/refrigerated)" AS __g2, "Transportation mode (land/cold chain)" AS __g3, COUNT(*) AS __a0 FROM "basic_drug_information"  GROUP BY "Origin / Tier (Domestic/Imported/JV)", "GSP Certification Status", "Storage conditions (room temperature/cool/refrigerated)", "Transportation mode (land/cold chain)";

-- S7
SELECT
  __g0 AS "origin",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c2"
GROUP BY
  __g0;

-- S21
SELECT
  __g1 AS "gsp",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c2"
GROUP BY
  __g1;

-- S22
SELECT
  __g2 AS "storage",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c2"
GROUP BY
  __g2;

-- S23
SELECT
  __g3 AS "transport",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c2"
GROUP BY
  __g3;

DROP TABLE temp."reuse_019_c2";

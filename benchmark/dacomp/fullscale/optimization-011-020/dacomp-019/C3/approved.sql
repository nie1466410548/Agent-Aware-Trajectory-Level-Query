-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_019_c3" AS
SELECT "Inventory Status (Normal/Frozen/Scrapped)" AS __g0, "Inventory Alert Status" AS __g1, "Inventory Discrepancy Rate" AS __g2, COUNT(*) AS __a0, MIN("Last Inbound Date") AS __a1, MAX("Last Inbound Date") AS __a2, MIN("Last Outbound Date") AS __a3, MAX("Last Outbound Date") AS __a4 FROM "inventory_management"  GROUP BY "Inventory Status (Normal/Frozen/Scrapped)", "Inventory Alert Status", "Inventory Discrepancy Rate";

-- S9
SELECT
  __g0 AS "status",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c3"
GROUP BY
  __g0;

-- S10
SELECT
  __g1 AS "alert",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c3"
GROUP BY
  __g1;

-- S20
SELECT
  MIN(__a1) AS "min_in",
  MAX(__a2) AS "max_in",
  MIN(__a3) AS "min_out",
  MAX(__a4) AS "max_out"
FROM temp."reuse_019_c3";

-- S26
SELECT
  __g2 AS "Inventory Discrepancy Rate",
  SUM(__a0) AS "cnt"
FROM temp."reuse_019_c3"
GROUP BY
  __g2
ORDER BY
  cnt DESC
LIMIT 15;

DROP TABLE temp."reuse_019_c3";

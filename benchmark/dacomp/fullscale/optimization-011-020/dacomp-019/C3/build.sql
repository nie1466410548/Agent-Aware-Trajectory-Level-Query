-- Execute once before S9; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_019_c3" AS
SELECT "Inventory Status (Normal/Frozen/Scrapped)" AS __g0, "Inventory Alert Status" AS __g1, "Inventory Discrepancy Rate" AS __g2, COUNT(*) AS __a0, MIN("Last Inbound Date") AS __a1, MAX("Last Inbound Date") AS __a2, MIN("Last Outbound Date") AS __a3, MAX("Last Outbound Date") AS __a4 FROM "inventory_management"  GROUP BY "Inventory Status (Normal/Frozen/Scrapped)", "Inventory Alert Status", "Inventory Discrepancy Rate";

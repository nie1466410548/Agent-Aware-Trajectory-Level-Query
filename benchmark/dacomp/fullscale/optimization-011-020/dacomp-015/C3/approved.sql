-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_015_c3" AS
SELECT * FROM data;

-- S22
SELECT "Featured", "Description", "Floor Plan", "Area", "Orientation", "Floor", "Decoration", "Location", "Watch Count", "Showings", "Date Published", "Price", "Price/sqm", "Remarks" FROM temp."reuse_015_c3";

-- S23
SELECT "Featured", "Description", "Floor Plan", "Area", "Orientation", "Floor", "Decoration", "Location", "Watch Count", "Showings", "Date Published", "Price", "Price/sqm", "Remarks" FROM temp."reuse_015_c3";

DROP TABLE temp."reuse_015_c3";

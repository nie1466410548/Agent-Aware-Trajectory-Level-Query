-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_016_c1" AS
SELECT * FROM "sheet1" WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018;

-- S7
SELECT
  "Year" AS "Year",
  "Region Name" AS "Region Name",
  "Surface Water Supply (100 million m³)" AS "Surface Water Supply (100 million m³)",
  "Groundwater Supply (100 million m³)" AS "Groundwater Supply (100 million m³)",
  "Total Water Supply (100 million m³)" AS "Total Water Supply (100 million m³)"
FROM temp."reuse_016_c1" AS sheet1
WHERE
  "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY
  "Year";

-- S11
SELECT
  "Year" AS "Year",
  ROUND(
    "Surface Water Supply (100 million m³)" / NULLIF("Groundwater Supply (100 million m³)", 0),
    4
  ) AS "Surface_to_Groundwater_Ratio",
  "Surface Water Supply (100 million m³)" AS "Surface",
  "Groundwater Supply (100 million m³)" AS "Groundwater",
  "Total Water Supply (100 million m³)" AS "Total"
FROM temp."reuse_016_c1" AS sheet1
WHERE
  "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY
  "Year";

DROP TABLE temp."reuse_016_c1";

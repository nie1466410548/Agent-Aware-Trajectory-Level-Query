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

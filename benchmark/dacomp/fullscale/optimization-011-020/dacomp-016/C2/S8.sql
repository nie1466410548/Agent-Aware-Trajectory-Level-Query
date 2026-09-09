SELECT
  "Year" AS "Year",
  "Region Name" AS "Region Name",
  "Urbanization rate (%)" AS "Urbanization rate (%)"
FROM temp."reuse_016_c2" AS economic_indicator_data
WHERE
  "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY
  "Year";

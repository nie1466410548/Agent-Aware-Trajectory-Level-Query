/* Check per capita GDP and industrial value added for China */
SELECT
  "Year" AS "Year",
  "Per capita GDP (yuan/person)" AS "Per capita GDP (yuan/person)",
  "Industrial value added (100 million yuan)" AS "Industrial value added (100 million yuan)",
  "Fixed asset investment (100 million yuan)" AS "Fixed asset investment (100 million yuan)",
  "Urbanization rate (%)" AS "Urbanization rate (%)"
FROM temp."reuse_016_c2" AS economic_indicator_data
WHERE
  "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY
  "Year";

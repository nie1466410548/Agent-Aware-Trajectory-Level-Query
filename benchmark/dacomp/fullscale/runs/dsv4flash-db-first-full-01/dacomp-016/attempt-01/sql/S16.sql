-- Check per capita GDP and industrial value added for China
SELECT "Year", "Per capita GDP (yuan/person)", "Industrial value added (100 million yuan)", "Fixed asset investment (100 million yuan)", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year"
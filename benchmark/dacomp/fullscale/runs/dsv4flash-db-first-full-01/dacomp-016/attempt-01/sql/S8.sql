SELECT "Year", "Region Name", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year"
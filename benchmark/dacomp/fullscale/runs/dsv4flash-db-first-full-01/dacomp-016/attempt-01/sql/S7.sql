SELECT "Year", "Region Name", "Surface Water Supply (100 million m³)", "Groundwater Supply (100 million m³)", "Total Water Supply (100 million m³)"
FROM sheet1
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year"
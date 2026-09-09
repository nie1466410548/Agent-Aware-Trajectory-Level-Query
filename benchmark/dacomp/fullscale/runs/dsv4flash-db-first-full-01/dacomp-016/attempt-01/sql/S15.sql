-- Check if other regions have the same urbanization pattern
SELECT "Region Name", "Year", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" IN ('Beijing Municipality', 'Shanghai Municipality', 'Guangdong Province', 'Hebei Province')
  AND "Year" IN (2005, 2010, 2015, 2018)
ORDER BY "Region Name", "Year"
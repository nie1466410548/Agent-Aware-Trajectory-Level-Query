SELECT 
  w."Year",
  w."Surface Water Supply (100 million m³)" AS Surface_Supply,
  w."Groundwater Supply (100 million m³)" AS Groundwater_Supply,
  w."Surface Water Supply (100 million m³)" / NULLIF(w."Groundwater Supply (100 million m³)", 0) AS Surf_GW_Ratio,
  e."Urbanization rate (%)" AS Urbanization_Rate
FROM sheet1 w
JOIN economic_indicator_data e
  ON w."Year" = e."Year" AND w."Region Name" = e."Region Name"
WHERE w."Region Name" = 'China' AND w."Year" BETWEEN 2005 AND 2018
ORDER BY w."Year"
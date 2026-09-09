SELECT e."Year",
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" AS ind_w,
       s."Total Water Consumption (100 million m³) " AS tot_w,
       ROUND(s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100, 2) AS ind_share_pct
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China'
ORDER BY e."Year"
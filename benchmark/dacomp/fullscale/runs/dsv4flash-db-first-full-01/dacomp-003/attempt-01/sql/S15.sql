SELECT COUNT(*) AS n, SUM(CASE WHEN s."Industrial Water Consumption (100 million m³)" IS NULL THEN 1 ELSE 0 END) AS null_ind,
       SUM(CASE WHEN s."Total Water Consumption (100 million m³) " IS NULL THEN 1 ELSE 0 END) AS null_tot,
       SUM(CASE WHEN e."Per capita GDP (yuan/person)" IS NULL THEN 1 ELSE 0 END) AS null_gdp
FROM sheet1 s LEFT JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
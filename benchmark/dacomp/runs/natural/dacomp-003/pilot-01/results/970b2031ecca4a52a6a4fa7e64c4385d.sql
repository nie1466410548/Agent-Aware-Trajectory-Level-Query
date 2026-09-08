SELECT e."Year" AS yr, e."Region Code" AS rcode, e."Region Name" AS rname,
e."Per capita GDP (yuan/person)" AS gdp_pc,
s."Industrial Water Consumption (100 million m³)" AS ind_wc,
s."Total Water Consumption (100 million m³) " AS tot_wc,
e."Urbanization rate (%)" AS urb,
e."Industrial value added (100 million yuan)" AS iva
FROM economic_indicator_data e
JOIN sheet1 s ON e."Year" = s."Year" AND e."Region Code" = s."Region Code"
ORDER BY rcode, yr;

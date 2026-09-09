-- Compare China urbanization with mean of provinces (potential aggregation check)
SELECT e."Year",
       (SELECT AVG("Urbanization rate (%)") FROM economic_indicator_data WHERE "Year" = e."Year" AND "Region Name" <> 'China') AS prov_avg_urban,
       MAX(CASE WHEN "Region Name" = 'China' THEN "Urbanization rate (%)" END) AS china_urban
FROM economic_indicator_data e
WHERE e."Year" IN (2005, 2010, 2014, 2018)
GROUP BY e."Year"
ORDER BY e."Year"
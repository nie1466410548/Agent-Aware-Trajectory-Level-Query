SELECT 
  'city' AS src, SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) AS pop6
FROM "2020_cn_city_pop_3_up_age_sex_e"
UNION ALL
SELECT 'town', SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END)
FROM "2020_cn_town_pop_3up_agesexedu"
UNION ALL
SELECT 'rural', SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END)
FROM "2020_cn_rural_pop_3up_agesexed"
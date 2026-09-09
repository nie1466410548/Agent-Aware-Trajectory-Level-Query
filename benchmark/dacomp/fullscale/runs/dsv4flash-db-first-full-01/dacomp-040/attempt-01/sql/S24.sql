SELECT 
  'city' AS src, SUM("Population Aged 6 and Over - Total") AS pop6
FROM "2010_cn_city_pop_6_up_age_sex_e"
UNION ALL
SELECT 'town', SUM("Population Aged 6 and Over - Total")
FROM "2010_cn_town_pop6up_agesexedu"
UNION ALL
SELECT 'rural', SUM("Population Aged 6 and Over - Total")
FROM "2010_cn_rural_6_up_age_sex_edu"
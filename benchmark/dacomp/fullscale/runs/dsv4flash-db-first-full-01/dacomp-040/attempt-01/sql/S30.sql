SELECT 
  'city' AS src,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) AS pop6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) AS never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) AS primary,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) AS junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) AS senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) AS jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) AS undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) AS masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) AS doctoral
FROM "2020_cn_city_pop_3_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_town_pop_3up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_rural_pop_3up_agesexed"
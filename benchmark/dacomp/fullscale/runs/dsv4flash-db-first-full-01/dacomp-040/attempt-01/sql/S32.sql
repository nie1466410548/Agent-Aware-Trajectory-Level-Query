SELECT 
  'city' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM("Primary School - Total") AS prim,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Junior College - Total") AS jcollege,
  SUM("Undergraduate - Total") AS undergrad,
  SUM("Postgraduate - Total") AS postgrad
FROM "2010_cn_city_pop_6_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_town_pop6up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_rural_6_up_age_sex_edu"
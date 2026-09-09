SELECT 
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM("Primary School - Total") AS primary_school,
  SUM("Junior High School - Total") AS junior_high
FROM "2000_cn_twn_pop_6_up_age_sex_ed"
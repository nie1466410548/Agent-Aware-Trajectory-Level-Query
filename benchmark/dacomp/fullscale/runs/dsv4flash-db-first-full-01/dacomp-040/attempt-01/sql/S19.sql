SELECT 
  SUM("Population Aged 6 and Over - Total") AS total_pop6,
  SUM("Never Attended School - Total") AS never_attended,
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)) AS literacy_class,
  SUM("Primary School - Total") AS primary_school,
  SUM("Junior High School - Total") AS junior_high,
  SUM("Senior High School - Total") AS senior_high,
  SUM("Vocational School - Total") AS vocational,
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)) AS junior_college,
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)) AS undergraduate,
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER)) AS postgraduate
FROM "2000_cn_pop_6_up_age_sex_edu"
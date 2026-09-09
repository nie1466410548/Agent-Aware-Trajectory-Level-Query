SELECT 
  SUM([Population Aged 3 and Over - Total]) AS total_pop3,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Population Aged 3 and Over - Total] ELSE 0 END) AS total_pop6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [ever Attended School - Total] ELSE 0 END) AS never_attended,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Preschool - Total] ELSE 0 END) AS preschool6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Primary School - Total] ELSE 0 END) AS primary_school,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Junior High School - Total] ELSE 0 END) AS junior_high,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Senior High School - Total] ELSE 0 END) AS senior_high,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Junior College - Total] ELSE 0 END) AS junior_college,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Undergraduate - Total] ELSE 0 END) AS undergraduate,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Master's Degree - Total] ELSE 0 END) AS masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Doctoral Degree - Total] ELSE 0 END) AS doctoral
FROM "2020_cn_pop_3_up_age_sex_edu"
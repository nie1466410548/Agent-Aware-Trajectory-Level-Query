SELECT 
  SUM([Population Aged 6 and Over - Total]) AS total_pop6,
  SUM([Never Attended School - Total]) AS never_attended,
  SUM([Primary School - Total]) AS primary_school,
  SUM([Junior High School - Total]) AS junior_high,
  SUM([Senior High School - Total]) AS senior_high,
  SUM([Junior College - Total]) AS junior_college,
  SUM([Undergraduate - Total]) AS undergraduate,
  SUM([Postgraduate - Total]) AS postgraduate
FROM "2010_cn_pop_6_up_age_sex_edu"
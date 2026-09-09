SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM("Never Attended School - Male") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM("Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Junior College - Male") AS male_jcollege,
  SUM(" Junior College - Female") AS female_jcollege,
  SUM("Undergraduate - Male") AS male_undergrad,
  SUM("Undergraduate - Female") AS female_undergrad,
  SUM("Postgraduate - Male") AS male_postgrad,
  SUM("Postgraduate - Female") AS female_postgrad
FROM "2010_cn_pop_6_up_age_sex_edu"
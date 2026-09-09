SELECT 
  'urban' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)) AS literacy,
  SUM("Primary School - Total") AS prim,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Vocational School - Total") AS vocational,
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)) AS jcollege,
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)) AS undergrad,
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER)) AS postgrad
FROM "2000_cn_pop_6_up_age_sex_eduurb"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000_cn_twn_pop_6_up_age_sex_ed"
UNION ALL
SELECT 'village',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000cnpop6upagesexeduvillage"
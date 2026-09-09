SELECT 
  'urban' AS src, SUM("Population Aged 6 and Over - Total") AS pop6
FROM "2000_cn_pop_6_up_age_sex_eduurb"
UNION ALL
SELECT 'village', SUM("Population Aged 6 and Over - Total")
FROM "2000cnpop6upagesexeduvillage"
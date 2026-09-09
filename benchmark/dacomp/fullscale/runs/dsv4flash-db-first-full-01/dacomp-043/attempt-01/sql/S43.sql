SELECT
  CASE WHEN "Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE 'No%' OR "Vaccination History (Doses/Date/Type)" LIKE 'None%' THEN 'No vaccination'
       ELSE 'Other' END AS vacc_cat,
  COUNT(*) AS n
FROM epidemiological_investigation
GROUP BY vacc_cat;
SELECT MIN(YearsAtCompany) AS min_years, 
       MAX(YearsAtCompany) AS max_years, 
       AVG(YearsAtCompany) AS avg_years,
       MEDIAN(YearsAtCompany) AS median_years
FROM sheet1
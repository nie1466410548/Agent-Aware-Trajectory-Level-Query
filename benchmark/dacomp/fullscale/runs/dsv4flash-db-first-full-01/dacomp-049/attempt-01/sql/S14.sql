SELECT * FROM (
  SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description"
  FROM sheet1 
  WHERE ("Industry" LIKE '%保险%' OR "Industry" = 'Insurance')
    AND "Industry" NOT LIKE '1800%'
    AND "Industry" NOT LIKE '1. Holiday%'
    AND "Industry" NOT LIKE 'Join Ctrip%'
    AND "Industry" NOT LIKE 'Other industries%'
    AND "Industry" NOT LIKE 'Internet/E-commerce%'
) AS insurance_jobs
ORDER BY "Job Title"
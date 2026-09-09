SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description" FROM sheet1
WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%')
  AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')
ORDER BY "Job Title"

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle'
       ELSE 'older' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  e."Missed Appointment" AS missed
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"

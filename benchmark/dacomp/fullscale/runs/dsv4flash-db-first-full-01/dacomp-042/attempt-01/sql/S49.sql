
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle (45-59)'
       ELSE 'Older (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  o."Satisfaction Rating" AS satisfaction
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"

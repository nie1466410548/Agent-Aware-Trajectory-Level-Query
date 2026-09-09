WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Financial stress", p."Stigma effect", p."Housing stability", p."Insurance status",
    p."Employment status", p."Living situation", p."Disability status", p."Education level", p."Marital Status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Financial stress", COUNT(*) n FROM joined GROUP BY age_group, "Financial stress" ORDER BY age_group, n DESC
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  id."Isolation Type (Home/Hospital/Centralized)" AS iso_type,
  id."Disinfection Frequency (times/day)" AS disinf_freq,
  id."Disinfectant Type (Chlorine-based/Peracetic Acid)" AS disinf_type,
  id."PPE Usage" AS ppe,
  id."Symptom Monitoring During Isolation" AS symp_monitor,
  COUNT(*) AS n
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp, iso_type, disinf_freq, disinf_type, ppe, symp_monitor
ORDER BY grp, n DESC;
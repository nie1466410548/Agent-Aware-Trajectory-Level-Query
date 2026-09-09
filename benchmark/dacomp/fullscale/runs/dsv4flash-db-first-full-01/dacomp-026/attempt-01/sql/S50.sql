SELECT 
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.medical') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS med_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.logistics') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS log_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.security') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS sec_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.volunteers') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),1) AS vol_ratio
FROM human_resources hr JOIN disaster_events de ON de."Disaster Event ID"=hr."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
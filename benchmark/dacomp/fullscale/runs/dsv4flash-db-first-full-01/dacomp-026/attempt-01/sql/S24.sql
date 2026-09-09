SELECT 
  ROUND(AVG("budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG("fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG("costbene(USD)"),2) AS avg_costbene,
  ROUND(AVG("opscosts(USD)"),0) AS avg_opscosts,
  ROUND(AVG("transportcosts(USD)"),0) AS avg_transport,
  ROUND(AVG("storagecosts(USD)"),0) AS avg_storage,
  ROUND(AVG("personnelcosts(USD)"),0) AS avg_personnel,
  ROUND(AVG("donorcommitments(USD)"),0) AS avg_donor,
  ROUND(AVG("resourcegaps(USD)"),0) AS avg_gaps,
  SUM(CASE WHEN "fundingstate"='Adequate' THEN 1 ELSE 0 END) AS funding_adequate,
  SUM(CASE WHEN "fundingstate"='Critical' THEN 1 ELSE 0 END) AS funding_critical,
  SUM(CASE WHEN "fundingstate"='Sufficient' THEN 1 ELSE 0 END) AS funding_sufficient
FROM financials1 fin JOIN disaster_events de ON de."Disaster Event ID" = fin."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
SELECT 
  MIN("costbene(USD)") AS min_cb, 
  ROUND(AVG("costbene(USD)"),1) AS avg_cb, 
  MAX("costbene(USD)") AS max_cb,
  ROUND(AVG("costbene(USD)"*1.0/NULLIF("budgetallot(USD)",0)),6) AS avg_benefit_cost_ratio
FROM financials1 fin JOIN disaster_events de ON de."Disaster Event ID"=fin."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
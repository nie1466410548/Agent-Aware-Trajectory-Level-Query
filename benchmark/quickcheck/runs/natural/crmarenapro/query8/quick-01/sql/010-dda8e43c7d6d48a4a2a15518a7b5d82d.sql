WITH period_owner_assignments AS (
  SELECT caseid__c, createddate, oldvalue__c, newvalue__c
  FROM casehistory__c
  WHERE field__c = 'Owner Assignment'
    AND createddate >= '2022-04-10'
    AND createddate <= '2023-04-10'
), transferred_cases AS (
  SELECT caseid__c
  FROM period_owner_assignments
  GROUP BY caseid__c
  HAVING COUNT(*) > 1
), handling_agents AS (
  SELECT DISTINCT p.newvalue__c AS agent_id
  FROM period_owner_assignments p
  JOIN transferred_cases t ON t.caseid__c = p.caseid__c
  WHERE p.newvalue__c IS NOT NULL
), transfer_counts AS (
  SELECT oldvalue__c AS agent_id, COUNT(*) AS transfer_count
  FROM period_owner_assignments
  WHERE oldvalue__c IS NOT NULL
  GROUP BY oldvalue__c
)
SELECT a.agent_id, COALESCE(t.transfer_count, 0) AS transfer_count
FROM handling_agents a
LEFT JOIN transfer_counts t ON t.agent_id = a.agent_id
ORDER BY transfer_count ASC, a.agent_id ASC
LIMIT 1;


WITH owner_assignments AS (
  SELECT caseid__c, createddate, oldvalue__c, newvalue__c
  FROM casehistory__c
  WHERE field__c = 'Owner Assignment'
    AND createddate >= '2022-04-01'
    AND createddate < '2023-04-01'
), handled AS (
  SELECT newvalue__c AS agent_id, COUNT(DISTINCT caseid__c) AS handled_cases
  FROM owner_assignments
  WHERE newvalue__c IS NOT NULL
  GROUP BY newvalue__c
), transfers AS (
  SELECT oldvalue__c AS agent_id, COUNT(*) AS transfer_count
  FROM owner_assignments
  WHERE oldvalue__c IS NOT NULL
  GROUP BY oldvalue__c
)
SELECT h.agent_id, h.handled_cases, COALESCE(t.transfer_count, 0) AS transfer_count
FROM handled h
LEFT JOIN transfers t ON t.agent_id = h.agent_id
ORDER BY transfer_count ASC, handled_cases ASC, agent_id ASC;


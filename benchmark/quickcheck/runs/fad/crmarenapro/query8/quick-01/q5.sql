WITH w AS (
  SELECT caseid__c, oldvalue__c, newvalue__c, createddate
  FROM casehistory__c
  WHERE field__c = 'Owner Assignment'
    AND createddate >= '2022-04-10' AND createddate < '2023-04-10'
),
handled AS (
  SELECT newvalue__c AS agent, COUNT(DISTINCT caseid__c) AS cases_handled
  FROM w GROUP BY newvalue__c
),
transfers AS (
  SELECT oldvalue__c AS agent, COUNT(*) AS transfer_count
  FROM w WHERE oldvalue__c IS NOT NULL
  GROUP BY oldvalue__c
)
SELECT t.agent, t.transfer_count, h.cases_handled
FROM transfers t
JOIN handled h ON h.agent = t.agent
WHERE h.cases_handled > 0
ORDER BY t.transfer_count ASC
LIMIT 5;

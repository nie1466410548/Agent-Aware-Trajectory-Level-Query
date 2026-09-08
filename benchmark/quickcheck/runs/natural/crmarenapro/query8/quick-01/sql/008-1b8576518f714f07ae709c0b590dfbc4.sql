SELECT caseid__c, createddate, oldvalue__c AS from_agent, newvalue__c AS to_agent
FROM casehistory__c
WHERE field__c='Owner Assignment'
  AND oldvalue__c IS NOT NULL
ORDER BY createddate, caseid__c;


SELECT h.caseid__c, h.createddate, h.oldvalue__c AS from_agent, h.newvalue__c AS to_agent,
       c.createddate AS case_createddate
FROM casehistory__c h
JOIN "Case" c ON c.id=h.caseid__c
WHERE h.field__c='Owner Assignment'
  AND h.oldvalue__c IS NOT NULL
ORDER BY h.createddate, h.caseid__c;


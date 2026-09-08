SELECT h.caseid__c, h.createddate, h.oldvalue__c, h.newvalue__c,
       c.ownerid AS current_ownerid, c.createddate AS case_createddate
FROM casehistory__c h
JOIN "Case" c ON c.id = h.caseid__c
WHERE h.field__c = 'Owner Assignment'
  AND h.createddate >= '2022-04-10'
  AND h.createddate <= '2023-04-10'
ORDER BY h.caseid__c, h.createddate, h.id;

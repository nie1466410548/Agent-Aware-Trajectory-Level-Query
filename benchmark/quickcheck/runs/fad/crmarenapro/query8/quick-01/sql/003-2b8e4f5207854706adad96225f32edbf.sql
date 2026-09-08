SELECT caseid__c, oldvalue__c, newvalue__c, createddate
FROM casehistory__c
WHERE field__c = 'Owner Assignment'
  AND createddate >= '2022-04-10'
  AND createddate < '2023-04-10'
ORDER BY caseid__c, createddate;


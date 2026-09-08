SELECT caseid__c, oldvalue__c, newvalue__c, createddate
FROM casehistory__c
WHERE field__c = 'Owner Assignment' AND oldvalue__c IS NOT NULL
ORDER BY createddate;


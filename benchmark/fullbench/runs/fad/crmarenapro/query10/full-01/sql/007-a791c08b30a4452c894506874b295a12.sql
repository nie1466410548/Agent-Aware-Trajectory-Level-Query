SELECT caseid__c, oldvalue__c, newvalue__c, createddate
FROM casehistory__c
WHERE field__c = 'Owner Assignment'
ORDER BY caseid__c, createddate;


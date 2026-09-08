SELECT MIN(createddate) AS mind, MAX(createddate) AS maxd, COUNT(*) AS total FROM casehistory__c WHERE field__c='Owner Assignment'

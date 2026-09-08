SELECT field__c, COUNT(*) AS n FROM casehistory__c GROUP BY field__c ORDER BY n DESC;


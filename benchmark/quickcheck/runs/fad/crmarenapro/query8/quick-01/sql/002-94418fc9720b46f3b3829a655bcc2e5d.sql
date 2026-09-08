SELECT field__c, COUNT(*) AS n, MIN(createddate) AS min_d, MAX(createddate) AS max_d
FROM casehistory__c
GROUP BY field__c
ORDER BY n DESC;


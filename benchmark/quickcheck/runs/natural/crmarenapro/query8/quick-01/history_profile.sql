SELECT field__c,
       COUNT(*) AS records,
       MIN(createddate) AS min_createddate,
       MAX(createddate) AS max_createddate,
       COUNT(DISTINCT oldvalue__c) AS distinct_old_values,
       COUNT(DISTINCT newvalue__c) AS distinct_new_values
FROM casehistory__c
GROUP BY field__c
ORDER BY records DESC;

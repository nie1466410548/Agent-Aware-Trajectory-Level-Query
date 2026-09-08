SELECT caseid__c, COUNT(*) AS owner_assignments
FROM casehistory__c
WHERE field__c = 'Owner Assignment'
GROUP BY caseid__c
ORDER BY owner_assignments DESC
LIMIT 20;

SELECT 'history' AS src, count(*) FROM casehistory__c WHERE caseid__c LIKE '%500Wt00000DDyznIAD%'
UNION ALL
SELECT 'email', count(*) FROM emailmessage WHERE parentid LIKE '%500Wt00000DDyznIAD%' OR relatedtoid LIKE '%500Wt00000DDyznIAD%'
UNION ALL
SELECT 'chat', count(*) FROM livechattranscript WHERE caseid LIKE '%500Wt00000DDyznIAD%';


SELECT 'history' AS src, id, caseid__c AS ref, field__c AS f1, oldvalue__c AS f2, newvalue__c AS f3, createddate::text AS ts FROM casehistory__c WHERE caseid__c = '#500Wt00000DDyznIAD'
UNION ALL
SELECT 'email', id, parentid, subject, fromaddress, left(textbody, 4000), messagedate::text FROM emailmessage WHERE parentid = '#500Wt00000DDyznIAD' OR relatedtoid = '#500Wt00000DDyznIAD'
UNION ALL
SELECT 'chat', id, caseid, 'chat', '', left(body, 6000), endtime::text FROM livechattranscript WHERE caseid = '#500Wt00000DDyznIAD'
ORDER BY ts;


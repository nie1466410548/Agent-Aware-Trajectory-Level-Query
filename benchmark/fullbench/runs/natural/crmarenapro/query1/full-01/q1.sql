SELECT Id, OpportunityId__c, LeadId__c, CreatedDate, EndTime__c, substr(Body__c,1,500) AS body_preview, length(Body__c) AS body_len
FROM VoiceCallTranscript__c
WHERE LeadId__c = '00QWt0000089AekMAE'
ORDER BY CreatedDate;

SELECT id, title, faq_answer__c FROM knowledge__kav WHERE lower(faq_answer__c) LIKE '%training%' AND (lower(faq_answer__c) LIKE '%access%' OR lower(faq_answer__c) LIKE '%policy%') LIMIT 20;

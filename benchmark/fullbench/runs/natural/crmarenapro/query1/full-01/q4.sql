SELECT id, title, summary, substr(faq_answer__c,1,2000) AS answer
FROM knowledge__kav
WHERE lower(title) LIKE '%qualif%' OR lower(title) LIKE '%bant%' OR lower(title) LIKE '%lead%'
   OR lower(summary) LIKE '%qualif%' OR lower(faq_answer__c) LIKE '%bant%';

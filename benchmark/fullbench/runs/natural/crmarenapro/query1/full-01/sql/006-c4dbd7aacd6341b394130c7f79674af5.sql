SELECT id, title, summary, faq_answer__c
FROM knowledge__kav
WHERE title ILIKE '%installation%timeline%' OR title ILIKE '%volume-based%';


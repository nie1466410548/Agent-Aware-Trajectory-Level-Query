SELECT id, title, summary, faq_answer__c FROM knowledge__kav WHERE title ILIKE '%scalab%' OR faq_answer__c ILIKE '%scalability enhancement%' OR summary ILIKE '%scalab%';

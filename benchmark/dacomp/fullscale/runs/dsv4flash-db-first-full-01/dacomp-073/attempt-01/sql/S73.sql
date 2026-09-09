SELECT status, 
       SUM(count_postings) as total_postings,
       SUM(count_offers) as total_offers
FROM lever__requisition_enhanced
GROUP BY status
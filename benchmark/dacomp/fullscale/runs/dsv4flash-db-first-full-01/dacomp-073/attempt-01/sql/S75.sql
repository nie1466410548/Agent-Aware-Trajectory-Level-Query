SELECT categories_department,
       SUM(count_requisitions) as total_requisitions,
       SUM(count_opportunities) as total_opportunities,
       SUM(count_open_opportunities) as total_open_opportunities,
       SUM(count_interviews) as total_interviews
FROM lever__posting_enhanced
GROUP BY categories_department
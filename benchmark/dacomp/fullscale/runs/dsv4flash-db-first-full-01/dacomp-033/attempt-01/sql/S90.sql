SELECT comp."Complaint Customer Satisfaction", COUNT(*) as cnt_all 
FROM complaints_table comp
GROUP BY comp."Complaint Customer Satisfaction"
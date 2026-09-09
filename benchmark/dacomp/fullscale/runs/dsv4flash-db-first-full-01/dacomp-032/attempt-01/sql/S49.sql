
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS speed_h,
cp."Complaint Customer Satisfaction" AS sat, cp."Whether Complaint Was Escalated" AS escalated,
cp."Complaint Type Serial Number" AS ctype
FROM complaints_table cp
JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID"
JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"

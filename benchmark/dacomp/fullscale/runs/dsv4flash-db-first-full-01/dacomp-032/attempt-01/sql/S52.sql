
SELECT t."Work Order ID", t."Ticket customer satisfaction score" AS ticket_sat,
t."Ticket resolution duration" AS res_h, cp."Complaint Customer Satisfaction" AS comp_sat,
cp."Complaint Type Serial Number" AS ctype,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS comp_speed
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
JOIN complaints_table cp ON cp."Work Order ID" = t."Work Order ID"
WHERE cc."Contact priority" = 1

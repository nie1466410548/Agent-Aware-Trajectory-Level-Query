
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu,
t."Ticket priority" AS tprio
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"

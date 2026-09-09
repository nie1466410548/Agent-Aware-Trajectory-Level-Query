SELECT s."Ticket customer satisfaction score", COUNT(*) as cnt_all
FROM service_ticket_table s
GROUP BY s."Ticket customer satisfaction score"
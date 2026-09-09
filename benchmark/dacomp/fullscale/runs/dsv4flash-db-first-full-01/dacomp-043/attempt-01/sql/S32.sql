SELECT "Contact Management (Yes/No)" AS contact_mgmt, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY contact_mgmt;
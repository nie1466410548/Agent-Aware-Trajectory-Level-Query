SELECT COUNT(DISTINCT r.recipient_email) AS resp_emails_in_contacts
FROM qualtrics__response r
JOIN qualtrics__contact c ON c.email = r.recipient_email
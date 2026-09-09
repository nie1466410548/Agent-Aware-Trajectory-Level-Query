-- Check if contact activity timestamps can be used for feature event tracking
SELECT last_activity_ts, last_replied_ts, last_contacted_ts, last_email_clicked_ts, last_email_opened_ts
FROM intercom__contact_enhanced LIMIT 10
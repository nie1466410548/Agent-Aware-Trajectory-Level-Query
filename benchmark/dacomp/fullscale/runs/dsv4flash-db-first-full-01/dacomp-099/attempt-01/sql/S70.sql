
SELECT ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count,
       cm.total_conversations, cm.avg_conversation_rating, cm.p50_time_to_first_response_min,
       cm.p50_reopens, cm.registration_retention_7d, cm.registration_retention_30d,
       cm.contacts_active_7d, cm.contacts_active_30d, cm.contacts_total
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id

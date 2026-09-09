SELECT ce.company_name, COUNT(*) as snapshots, COUNT(DISTINCT ce.plan_name) as plans, GROUP_CONCAT(DISTINCT ce.plan_name) as plan_list
FROM intercom__company_enhanced ce
WHERE ce.company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
GROUP BY ce.company_name
ORDER BY snapshots DESC
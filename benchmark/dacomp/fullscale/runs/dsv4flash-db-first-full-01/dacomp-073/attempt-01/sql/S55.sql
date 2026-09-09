SELECT COUNT(*) as cnt
FROM lever__requisition_enhanced r
WHERE r.hiring_manager_user_id IN (SELECT creator_user_id FROM lever__posting_enhanced)
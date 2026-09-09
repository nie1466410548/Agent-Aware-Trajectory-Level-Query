SELECT COUNT(DISTINCT r.hiring_manager_user_id) as matched_hm
FROM lever__requisition_enhanced r
WHERE r.hiring_manager_user_id IN (SELECT creator_user_id FROM lever__posting_enhanced)
   OR r.hiring_manager_user_id IN (SELECT owner_user_id FROM lever__posting_enhanced)
SELECT COUNT(*) as overlap
FROM lever__requisition_enhanced r
WHERE r.owner_name IN (SELECT DISTINCT posting_hiring_manager_name FROM lever__posting_enhanced)
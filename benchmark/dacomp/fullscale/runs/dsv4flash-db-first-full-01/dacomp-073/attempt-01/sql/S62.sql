SELECT COUNT(*) as total_hiring_managers
FROM (SELECT DISTINCT posting_hiring_manager_name FROM lever__posting_enhanced)
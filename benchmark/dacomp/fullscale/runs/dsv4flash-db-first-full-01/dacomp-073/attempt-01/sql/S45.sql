SELECT COUNT(DISTINCT p.requisition_code) as matched_codes
FROM lever__posting_enhanced p
JOIN lever__requisition_enhanced r ON p.requisition_code = r.requisition_code
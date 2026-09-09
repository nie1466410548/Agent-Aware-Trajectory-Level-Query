SELECT COUNT(DISTINCT r.team) as req_team_cnt
FROM lever__requisition_enhanced r
JOIN lever__posting_enhanced p ON r.team = p.categories_team
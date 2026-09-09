SELECT COUNT(DISTINCT r.team) as req_team_in_post_team
FROM lever__requisition_enhanced r
WHERE r.team IN (SELECT categories_team FROM lever__posting_enhanced)
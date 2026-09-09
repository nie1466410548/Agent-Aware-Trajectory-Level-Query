SELECT COUNT(DISTINCT vf.visitor_id) AS vf_visitors_not_in_visitor
FROM pendo__visitor_feature vf
LEFT JOIN pendo__visitor v ON vf.visitor_id = v.visitor_id
WHERE v.visitor_id IS NULL
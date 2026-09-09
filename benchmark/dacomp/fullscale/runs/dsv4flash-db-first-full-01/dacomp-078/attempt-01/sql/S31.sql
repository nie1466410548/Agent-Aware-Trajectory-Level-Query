SELECT COUNT(DISTINCT vf.visitor_id) AS vf_in_visitor
FROM pendo__visitor_feature vf
JOIN pendo__visitor v ON vf.visitor_id = v.visitor_id
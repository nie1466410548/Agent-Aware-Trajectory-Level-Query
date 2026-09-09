SELECT COUNT(DISTINCT account_id) AS accts_with_vf
FROM pendo__visitor v JOIN pendo__visitor_feature vf ON v.visitor_id = vf.visitor_id
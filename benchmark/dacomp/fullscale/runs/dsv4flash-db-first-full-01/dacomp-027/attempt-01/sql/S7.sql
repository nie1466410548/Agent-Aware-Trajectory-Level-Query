SELECT
 (SELECT COUNT(*) FROM disaster_events) AS events,
 (SELECT COUNT(*) FROM coordination_and_evaluation) AS coord,
 (SELECT COUNT(*) FROM environment_and_health) AS env,
 (SELECT COUNT(*) FROM operations1) AS ops,
 (SELECT COUNT(*) FROM financials1) AS fin,
 (SELECT COUNT(*) FROM distribution_hubs) AS hubs,
 (SELECT COUNT(*) FROM transportation1) AS trans,
 (SELECT COUNT(*) FROM supplies1) AS sup,
 (SELECT COUNT(*) FROM human_resources) AS hr,
 (SELECT COUNT(*) FROM beneficiaries_and_assessments) AS ben
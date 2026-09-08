WITH cases AS (
  SELECT id, ownerid,
         substring(createddate,1,19)::timestamp AS created,
         CASE WHEN closeddate IS NOT NULL THEN substring(closeddate,1,19)::timestamp END AS closed
  FROM "Case"
  WHERE substring(createddate,1,19)::timestamp >= TIMESTAMP '2023-05-02 00:00:00'
),
assign AS (
  SELECT caseid__c, COUNT(*) AS n_assign
  FROM casehistory__c
  WHERE field__c = 'Owner Assignment'
  GROUP BY caseid__c
),
-- cases handled per agent (both initial and transferred-to) within window
agent_cases AS (
  SELECT h.newvalue__c AS agent_id, COUNT(DISTINCT h.caseid__c) AS n_cases
  FROM casehistory__c h
  JOIN cases c ON c.id = h.caseid__c
  WHERE h.field__c = 'Owner Assignment' AND h.newvalue__c IS NOT NULL
  GROUP BY h.newvalue__c
),
eligible AS (
  SELECT agent_id FROM agent_cases WHERE n_cases > 1
),
ht AS (
  SELECT c.ownerid AS agent_id,
         EXTRACT(EPOCH FROM (c.closed - c.created)) AS secs
  FROM cases c
  JOIN assign a ON a.caseid__c = c.id
  WHERE a.n_assign = 1 AND c.closed IS NOT NULL
)
SELECT ht.agent_id, AVG(ht.secs) AS avg_secs, COUNT(*) AS n_timed
FROM ht
JOIN eligible e ON e.agent_id = ht.agent_id
GROUP BY ht.agent_id
ORDER BY avg_secs;


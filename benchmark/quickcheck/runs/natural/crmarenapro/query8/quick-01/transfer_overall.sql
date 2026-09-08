WITH a AS (
  SELECT caseid__c, createddate, oldvalue__c, newvalue__c,
         SUBSTR(createddate, 1, 4) AS yr,
         CAST(SUBSTR(createddate, 6, 2) AS INTEGER) AS mo
  FROM casehistory__c
  WHERE field__c = 'Owner Assignment'
), q AS (
  SELECT *, yr || '-Q' || CAST(((mo - 1) / 3 + 1) AS TEXT) AS quarter FROM a
), handled AS (
  SELECT newvalue__c agent_id, COUNT(DISTINCT caseid__c) handled_cases_all
  FROM a WHERE newvalue__c IS NOT NULL GROUP BY newvalue__c
), transfers AS (
  SELECT oldvalue__c agent_id, COUNT(*) transfer_count_all
  FROM a WHERE oldvalue__c IS NOT NULL GROUP BY oldvalue__c
), quarter_transfers AS (
  SELECT quarter, oldvalue__c agent_id, COUNT(*) transfers
  FROM q WHERE oldvalue__c IS NOT NULL GROUP BY quarter, oldvalue__c
)
SELECT h.agent_id, h.handled_cases_all, COALESCE(t.transfer_count_all, 0) transfer_count_all,
       COALESCE(STRING_AGG(qt.quarter || ':' || qt.transfers, ', ' ORDER BY qt.quarter), '') AS transfers_by_quarter
FROM handled h
LEFT JOIN transfers t ON t.agent_id=h.agent_id
LEFT JOIN quarter_transfers qt ON qt.agent_id=h.agent_id
GROUP BY h.agent_id, h.handled_cases_all, t.transfer_count_all
ORDER BY transfer_count_all DESC, agent_id;

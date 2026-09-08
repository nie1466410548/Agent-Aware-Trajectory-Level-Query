SELECT
  COUNT(*) AS opp_with_contract,
  SUM(CASE WHEN c1.Id IS NOT NULL THEN 1 ELSE 0 END) AS matched_raw,
  SUM(CASE WHEN c2.Id IS NOT NULL THEN 1 ELSE 0 END) AS matched_stripped
FROM Opportunity o
LEFT JOIN Contract c1 ON c1.Id = o.ContractID__c
LEFT JOIN Contract c2 ON replace(c2.Id, '#', '') = replace(o.ContractID__c, '#', '')
WHERE o.ContractID__c IS NOT NULL;


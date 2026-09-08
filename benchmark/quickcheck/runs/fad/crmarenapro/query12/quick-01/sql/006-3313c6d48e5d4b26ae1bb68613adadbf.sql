SELECT
  SUM(CASE WHEN ContractID__c LIKE '#%' THEN 1 ELSE 0 END) AS hash_contract,
  SUM(CASE WHEN OwnerId LIKE '#%' THEN 1 ELSE 0 END) AS hash_owner,
  COUNT(*) AS total
FROM Opportunity;

SELECT
  SUM(CASE WHEN Id LIKE '#%' THEN 1 ELSE 0 END) AS hash_id,
  COUNT(*) AS total
FROM Contract;


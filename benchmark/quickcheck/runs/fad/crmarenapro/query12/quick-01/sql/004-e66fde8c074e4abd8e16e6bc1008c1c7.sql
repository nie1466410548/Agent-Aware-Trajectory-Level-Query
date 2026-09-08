SELECT
  MIN(CreatedDate) AS min_created, MAX(CreatedDate) AS max_created,
  MIN(CloseDate) AS min_close, MAX(CloseDate) AS max_close,
  COUNT(*) AS n_opp,
  SUM(CASE WHEN ContractID__c IS NOT NULL THEN 1 ELSE 0 END) AS n_with_contract,
  SUM(CASE WHEN CAST(CreatedDate AS DATE) >= DATE '2023-04-01' AND CAST(CreatedDate AS DATE) < DATE '2023-05-01' THEN 1 ELSE 0 END) AS n_created_apr2023,
  SUM(CASE WHEN CAST(CloseDate AS DATE) >= DATE '2023-04-01' AND CAST(CloseDate AS DATE) < DATE '2023-05-01' THEN 1 ELSE 0 END) AS n_closed_apr2023
FROM Opportunity;


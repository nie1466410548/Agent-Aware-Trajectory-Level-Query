SELECT
  MIN(o.CreatedDate) AS min_created, MAX(o.CreatedDate) AS max_created,
  MIN(o.CloseDate) AS min_close, MAX(o.CloseDate) AS max_close,
  COUNT(*) AS n_opp,
  SUM(CASE WHEN o.ContractID__c IS NOT NULL THEN 1 ELSE 0 END) AS n_with_contract
FROM Opportunity o;

SELECT
  MIN(c.CompanySignedDate) AS min_signed, MAX(c.CompanySignedDate) AS max_signed,
  COUNT(*) AS n_contract
FROM Contract c;

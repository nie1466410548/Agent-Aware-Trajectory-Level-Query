SELECT
  o.Id AS opp_id, o.OwnerId, o.CreatedDate, o.CloseDate, c.CompanySignedDate,
  CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE) AS cycle_days
FROM Opportunity o
JOIN Contract c ON c.Id = o.ContractID__c
WHERE CAST(o.CloseDate AS DATE) >= DATE '2023-04-01'
  AND CAST(o.CloseDate AS DATE) < DATE '2023-05-01'
ORDER BY o.OwnerId;

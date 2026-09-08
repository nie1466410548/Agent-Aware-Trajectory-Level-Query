SELECT
  o.OwnerId,
  COUNT(*) AS n_opps,
  AVG(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS avg_cycle_days
FROM Opportunity o
JOIN Contract c ON replace(c.Id, '#', '') = replace(o.ContractID__c, '#', '')
WHERE CAST(c.CompanySignedDate AS DATE) >= DATE '2023-04-01'
  AND CAST(c.CompanySignedDate AS DATE) < DATE '2023-05-01'
GROUP BY o.OwnerId
ORDER BY avg_cycle_days ASC;


SELECT
  o.OwnerId,
  COUNT(*) AS n_opps,
  AVG(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS avg_cycle_days,
  MIN(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS min_cycle,
  MAX(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS max_cycle
FROM Opportunity o
JOIN Contract c ON replace(c.Id, '#', '') = replace(o.ContractID__c, '#', '')
WHERE CAST(o.CreatedDate AS DATE) >= DATE '2023-04-01'
  AND CAST(o.CreatedDate AS DATE) < DATE '2023-05-01'
  AND c.CompanySignedDate IS NOT NULL
GROUP BY o.OwnerId
ORDER BY avg_cycle_days ASC;


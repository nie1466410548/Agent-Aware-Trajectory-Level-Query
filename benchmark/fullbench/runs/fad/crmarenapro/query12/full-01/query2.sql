SELECT o.OwnerId,
       COUNT(*) AS n_opps,
       AVG(date_diff('day', CAST(o.CreatedDate AS DATE), CAST(c.CompanySignedDate AS DATE))) AS avg_days
FROM Opportunity o
JOIN Contract c ON o.ContractID__c = c.Id
WHERE CAST(c.CompanySignedDate AS DATE) >= DATE '2023-04-01'
  AND CAST(c.CompanySignedDate AS DATE) < DATE '2023-05-01'
GROUP BY o.OwnerId
ORDER BY avg_days ASC;

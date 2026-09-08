SELECT o.OwnerId, COUNT(*) AS n, AVG(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS avg_days
FROM Opportunity o
JOIN Contract c ON o.ContractID__c = c.Id
WHERE o.CloseDate >= '2023-04-01' AND o.CloseDate < '2023-05-01'
GROUP BY o.OwnerId
ORDER BY avg_days;


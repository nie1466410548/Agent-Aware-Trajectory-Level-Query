SELECT REPLACE(o.OwnerId,'#','') AS OwnerId, COUNT(*) AS n,
       AVG(CAST(c.CompanySignedDate AS DATE) - CAST(o.CreatedDate AS DATE)) AS avg_days
FROM Opportunity o
JOIN Contract c ON REPLACE(o.ContractID__c,'#','') = REPLACE(c.Id,'#','')
WHERE o.CreatedDate >= '2023-04-01' AND o.CreatedDate < '2023-05-01'
GROUP BY REPLACE(o.OwnerId,'#','')
ORDER BY avg_days;


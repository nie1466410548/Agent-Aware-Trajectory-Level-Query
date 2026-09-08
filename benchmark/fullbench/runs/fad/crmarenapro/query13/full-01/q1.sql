SELECT o.Id AS OpportunityId, o.AccountId, o.OwnerId, c.CompanySignedDate
FROM Opportunity o
JOIN Contract c ON o.ContractID__c = c.Id
WHERE CAST(c.CompanySignedDate AS DATE) BETWEEN DATE '2022-06-25' AND DATE '2022-11-25'

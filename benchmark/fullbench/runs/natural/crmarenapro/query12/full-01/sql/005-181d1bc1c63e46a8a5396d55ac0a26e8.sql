SELECT Id, OwnerId, ContractID__c, StageName, CreatedDate, CloseDate FROM Opportunity
WHERE CreatedDate >= '2023-04-01' AND CreatedDate < '2023-05-01';


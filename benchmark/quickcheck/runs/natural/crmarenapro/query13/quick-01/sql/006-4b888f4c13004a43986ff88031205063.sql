SELECT COUNT(*) AS n_opp, COUNT(DISTINCT AccountId) AS accts, COUNT(DISTINCT ContractID__c) AS contracts, COUNT(DISTINCT OwnerId) AS owners FROM Opportunity

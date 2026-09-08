SELECT o.AccountId, COUNT(*) AS n_opp, COUNT(DISTINCT o.ContractID__c) AS n_con FROM Opportunity o GROUP BY o.AccountId ORDER BY n_opp DESC LIMIT 5

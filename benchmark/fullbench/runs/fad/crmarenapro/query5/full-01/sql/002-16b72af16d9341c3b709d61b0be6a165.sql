SELECT id, orderitemid__c, issueid__c, createddate FROM "Case" WHERE createddate >= '2022-08-16' AND createddate <= '2023-01-16' AND orderitemid__c IS NOT NULL

SELECT id, issueid__c, orderitemid__c, createddate FROM "Case" WHERE orderitemid__c IS NOT NULL AND createddate >= '2022-08-16';

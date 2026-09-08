SELECT id, issueid__c, orderitemid__c, createddate FROM "case" WHERE orderitemid__c IS NOT NULL AND createddate >= '2022-08-16';


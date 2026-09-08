SELECT o.Id, o.Name, o.StageName, o.CloseDate, oli.Product2Id, oli.Quantity, oli.TotalPrice
FROM Opportunity o JOIN OpportunityLineItem oli ON oli.OpportunityId = o.Id
WHERE (o.ContactId = '003Wt00000Jqy8SIAR' OR o.AccountId IN ('001Wt00000PGXrNIAX','#001Wt00000PGXrNIAX'))
  AND o.CloseDate BETWEEN '2021-06-01' AND '2021-06-30'

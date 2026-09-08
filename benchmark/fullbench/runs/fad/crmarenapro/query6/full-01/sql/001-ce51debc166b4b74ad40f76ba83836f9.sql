SELECT q.Id, q.OpportunityId, q.AccountId, q.ContactId, q.Name, q.Status, q.Description,
       qli.Id AS QLI_Id, qli.Product2Id, qli.PricebookEntryId, qli.Quantity, qli.UnitPrice, qli.Discount, qli.TotalPrice
FROM Quote q
JOIN QuoteLineItem qli ON qli.QuoteId = q.Id
WHERE q.Id = '0Q0Wt000001WRAzKAO'

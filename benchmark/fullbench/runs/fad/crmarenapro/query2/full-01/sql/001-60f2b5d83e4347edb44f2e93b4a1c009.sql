SELECT q.*, qli.Id as QliId, qli.Product2Id, qli.Quantity, qli.UnitPrice, qli.Discount, qli.TotalPrice
FROM Quote q
LEFT JOIN QuoteLineItem qli ON qli.QuoteId = q.Id
WHERE q.Id = '0Q0Wt000001WSDVKA4';


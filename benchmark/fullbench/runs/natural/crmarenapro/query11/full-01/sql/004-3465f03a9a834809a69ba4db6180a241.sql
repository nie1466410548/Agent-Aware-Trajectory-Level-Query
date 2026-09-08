SELECT o.Id AS OrderId, o.AccountId, o.Status, o.EffectiveDate, oi.Product2Id, oi.Quantity, oi.UnitPrice
FROM "Order" o JOIN OrderItem oi ON oi.OrderId = o.Id
WHERE o.AccountId IN ('001Wt00000PGXrNIAX', '#001Wt00000PGXrNIAX')
ORDER BY o.EffectiveDate


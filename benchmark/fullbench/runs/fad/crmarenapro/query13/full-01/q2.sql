SELECT o.Id AS OrderId, o.AccountId, o.OwnerId, o.EffectiveDate, o.Status,
       SUM(oi.Quantity * oi.UnitPrice) AS SalesAmount
FROM "Order" o
JOIN OrderItem oi ON oi.OrderId = o.Id
GROUP BY o.Id, o.AccountId, o.OwnerId, o.EffectiveDate, o.Status

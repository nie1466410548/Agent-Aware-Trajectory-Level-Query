SELECT DISTINCT o.AccountId
FROM "Order" o
JOIN OrderItem oi ON oi.OrderId = o.Id
WHERE oi.Product2Id = '01tWt000006hVJdIAM';


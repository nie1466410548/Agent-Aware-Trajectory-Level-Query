SELECT oi.Id AS order_item_id, oi.OrderId, oi.Product2Id, oi.Quantity, oi.UnitPrice,
       o.AccountId, o.Status, o.EffectiveDate, o.OwnerId,
       p.Name AS product_name
FROM OrderItem oi
JOIN "Order" o ON oi.OrderId = o.Id
LEFT JOIN Product2 p ON oi.Product2Id = p.Id
WHERE oi.Id LIKE '%802Wt000007928FIAQ%';


SELECT oi.Id, oi.OrderId, oi.Product2Id
FROM OrderItem oi
WHERE oi.OrderId IN (
  SELECT DISTINCT OrderId FROM OrderItem WHERE Product2Id = '01tWt000006hVJdIAM'
);

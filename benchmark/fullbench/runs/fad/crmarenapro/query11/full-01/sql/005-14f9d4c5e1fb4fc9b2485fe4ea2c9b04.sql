SELECT oi.Id AS OrderItemId, oi.Product2Id, p.Name, p.Description, oi.Quantity, oi.UnitPrice FROM OrderItem oi JOIN Product2 p ON p.Id = oi.Product2Id WHERE oi.OrderId = '801Wt00000PHRYWIA5'

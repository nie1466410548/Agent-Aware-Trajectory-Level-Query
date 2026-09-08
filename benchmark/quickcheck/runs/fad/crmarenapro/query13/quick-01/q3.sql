SELECT 'rolling_2022-06-25_to_2022-11-25' AS variant, o.OwnerId, SUM(oi.Quantity*oi.UnitPrice) AS total
FROM "Order" o JOIN OrderItem oi ON oi.OrderId=o.Id
WHERE o.EffectiveDate >= '2022-06-25' AND o.EffectiveDate <= '2022-11-25'
GROUP BY o.OwnerId
UNION ALL
SELECT 'cal_months_jun_to_nov', o.OwnerId, SUM(oi.Quantity*oi.UnitPrice)
FROM "Order" o JOIN OrderItem oi ON oi.OrderId=o.Id
WHERE o.EffectiveDate >= '2022-06-01' AND o.EffectiveDate <= '2022-11-30'
GROUP BY o.OwnerId
UNION ALL
SELECT 'last5_full_months_jun_to_oct', o.OwnerId, SUM(oi.Quantity*oi.UnitPrice)
FROM "Order" o JOIN OrderItem oi ON oi.OrderId=o.Id
WHERE o.EffectiveDate >= '2022-06-01' AND o.EffectiveDate <= '2022-10-31'
GROUP BY o.OwnerId
ORDER BY variant, total DESC;

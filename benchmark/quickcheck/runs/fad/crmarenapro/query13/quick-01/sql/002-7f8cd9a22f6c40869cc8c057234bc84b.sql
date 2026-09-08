SELECT MIN(EffectiveDate) AS min_date, MAX(EffectiveDate) AS max_date, COUNT(*) AS n_orders, COUNT(DISTINCT OwnerId) AS n_owners FROM "Order";


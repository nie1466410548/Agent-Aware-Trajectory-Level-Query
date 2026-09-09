SELECT strftime('%Y', "Transaction Date") AS yr, COUNT(*) AS n, SUM("Sales Quantity (units)") AS total_qty
FROM core_transaction_information
GROUP BY yr
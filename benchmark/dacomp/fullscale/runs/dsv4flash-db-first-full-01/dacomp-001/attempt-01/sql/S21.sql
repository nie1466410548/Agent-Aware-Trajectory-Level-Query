
SELECT "Enterprise Code" AS code, strftime('%Y', "Invoice Date") AS yr, SUM("Amount Including Tax") AS rev
FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice'
GROUP BY "Enterprise Code", yr

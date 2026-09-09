-- Check if nch companies are buyers from ch companies
SELECT COUNT(DISTINCT s."Buyer organization code") AS n_nch_buyers
FROM ch___sales_invoices s
WHERE s."Buyer organization code" IN (SELECT "Enterprise Code" FROM nch___company_info)
  AND s."Invoice Status" = 'Valid Invoice'
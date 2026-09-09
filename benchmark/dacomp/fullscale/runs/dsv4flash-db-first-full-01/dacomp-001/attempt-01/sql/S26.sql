-- Check if nch companies are suppliers to ch companies
SELECT COUNT(DISTINCT i."Seller Organization Code") AS n_nch_suppliers
FROM ch___input_invoices i
WHERE i."Seller Organization Code" IN (SELECT "Enterprise Code" FROM nch___company_info)
  AND i."Invoice Status" = 'Valid Invoice'
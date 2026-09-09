WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT 
  (SELECT COUNT(*) FROM hv) as total_hv,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM membership_table)) as in_membership,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_tag_table)) as in_tags,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_contact_table)) as in_contact,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM contracts_table)) as in_contracts,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM financials_table)) as in_financials,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM product_service_order_table)) as in_orders,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_account_table)) as in_accounts,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM sales_follow_up_table)) as in_followup
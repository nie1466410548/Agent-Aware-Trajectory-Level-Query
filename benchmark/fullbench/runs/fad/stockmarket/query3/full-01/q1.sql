SELECT 'FinancialStatus' AS kind, "Financial Status" AS val, COUNT(*) AS cnt FROM stockinfo GROUP BY "Financial Status"
UNION ALL
SELECT 'ListingExchange' AS kind, "Listing Exchange" AS val, COUNT(*) AS cnt FROM stockinfo GROUP BY "Listing Exchange"
UNION ALL
SELECT 'NasdaqTraded' AS kind, "Nasdaq Traded" AS val, COUNT(*) AS cnt FROM stockinfo GROUP BY "Nasdaq Traded";

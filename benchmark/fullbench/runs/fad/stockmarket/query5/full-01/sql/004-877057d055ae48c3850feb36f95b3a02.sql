SELECT "Symbol", "Company Description", "ETF"
FROM stockinfo
WHERE "Market Category" = 'S' AND "Listing Exchange" = 'Q'
ORDER BY "Symbol";


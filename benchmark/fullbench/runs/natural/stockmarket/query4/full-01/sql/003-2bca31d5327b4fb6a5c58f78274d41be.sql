SELECT "Symbol", "Listing Exchange", "ETF", "Company Description" FROM stockinfo WHERE "Listing Exchange" = 'N' OR "Listing Exchange" LIKE '%NYSE%';


SELECT "Symbol", "Company Description", "Financial Status" FROM stockinfo
WHERE "Listing Exchange" = 'Q' AND "Financial Status" IS NOT NULL AND "Financial Status" <> 'N'
ORDER BY "Symbol";

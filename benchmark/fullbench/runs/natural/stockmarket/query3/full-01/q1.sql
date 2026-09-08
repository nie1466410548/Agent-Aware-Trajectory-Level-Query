SELECT "Financial Status", "Listing Exchange", "Nasdaq Traded", "Market Category", COUNT(*) FROM stockinfo GROUP BY 1,2,3,4 ORDER BY 1;

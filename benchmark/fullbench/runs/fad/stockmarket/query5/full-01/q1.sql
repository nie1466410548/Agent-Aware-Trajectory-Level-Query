SELECT "Market Category", "Listing Exchange", COUNT(*) AS n
FROM stockinfo
GROUP BY "Market Category", "Listing Exchange"
ORDER BY n DESC;

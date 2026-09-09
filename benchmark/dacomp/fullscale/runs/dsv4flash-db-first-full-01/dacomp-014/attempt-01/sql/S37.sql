SELECT "Main Category", COUNT(*) as cnt, MIN("Rank") as min_rank, MAX("Rank") as max_rank, COUNT(DISTINCT "Rank") as distinct_ranks
FROM sheet1
GROUP BY "Main Category"
ORDER BY cnt DESC
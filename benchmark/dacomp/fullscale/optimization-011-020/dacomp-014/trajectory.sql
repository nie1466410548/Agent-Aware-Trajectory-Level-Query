-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.

-- S3
SELECT * FROM sheet1 LIMIT 20;

-- S4
SELECT COUNT(*) as total_rows FROM sheet1;

-- S5
SELECT DISTINCT "Video Category" FROM sheet1 ORDER BY "Video Category";

-- S6
SELECT DISTINCT "Main Category" FROM sheet1 ORDER BY "Main Category";

-- S7
SELECT DISTINCT "Creator Gender" FROM sheet1 ORDER BY "Creator Gender";

-- S8
SELECT DISTINCT "Bilibili Personal Verification" FROM sheet1 ORDER BY "Bilibili Personal Verification";

-- S9
SELECT MIN("Rank") as min_rank, MAX("Rank") as max_rank FROM sheet1;

-- S10
SELECT DISTINCT _id FROM sheet1 LIMIT 10;

-- S11
SELECT 
  MIN("Views") as min_views, 
  AVG("Views") as avg_views, 
  MAX("Views") as max_views,
  MIN("Likes") as min_likes,
  AVG("Likes") as avg_likes,
  MAX("Likes") as max_likes,
  MIN("Coins") as min_coins,
  AVG("Coins") as avg_coins,
  MAX("Coins") as max_coins,
  MIN("Favorites") as min_fav,
  AVG("Favorites") as avg_fav,
  MAX("Favorites") as max_fav,
  MIN("Shares") as min_shares,
  AVG("Shares") as avg_shares,
  MAX("Shares") as max_shares,
  MIN("Comments") as min_comments,
  AVG("Comments") as avg_comments,
  MAX("Comments") as max_comments,
  MIN("Danmaku Count") as min_danmaku,
  AVG("Danmaku Count") as avg_danmaku,
  MAX("Danmaku Count") as max_danmaku
FROM sheet1;

-- S12
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
ORDER BY avg_views DESC
LIMIT 20;

-- S13
SELECT 
  "Main Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY "Main Category"
ORDER BY avg_views DESC;

-- S14
SELECT 
  "Creator Gender",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator Gender";

-- S15
SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as verification_status,
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers
FROM sheet1
GROUP BY verification_status;

-- S16
SELECT 
  "Creator Video Count",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares
FROM sheet1
GROUP BY "Creator Video Count"
ORDER BY "Creator Video Count" DESC
LIMIT 20;

-- S17
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY avg_views DESC
LIMIT 20;

-- S18
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate,
  ROUND(1.0*AVG("Comments")/AVG("Views")*100, 2) as comment_rate,
  ROUND(1.0*AVG("Danmaku Count")/AVG("Views")*100, 2) as danmaku_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY like_rate DESC
LIMIT 20;

-- S19
SELECT 
  CASE WHEN "Rank" <= 10 THEN 'Top 10'
       WHEN "Rank" <= 30 THEN '11-30'
       WHEN "Rank" <= 50 THEN '31-50'
       WHEN "Rank" <= 70 THEN '51-70'
       ELSE '71-100' END as rank_band,
  "Main Category",
  COUNT(*) as count
FROM sheet1
GROUP BY rank_band, "Main Category"
ORDER BY rank_band, count DESC;

-- S20
SELECT "Title", "Creator", "Views", "Likes", "Coins", "Shares", "Favorites", "Danmaku Count", "Comments", "Overall Score", "Video Category", "Creator Followers"
FROM sheet1
ORDER BY "Views" DESC
LIMIT 20;

-- S21
SELECT 
  ROUND(AVG("Overall Score")) as avg_overall_score,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Total Views")) as avg_creator_views,
  ROUND(AVG("Creator Total Likes")) as avg_creator_likes,
  ROUND(AVG("Creator Video Count")) as avg_creator_videos
FROM sheet1
WHERE "Rank" <= 10;

-- S22
SELECT 
  ROUND(AVG("Overall Score")) as avg_overall_score,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Total Views")) as avg_creator_views,
  ROUND(AVG("Creator Total Likes")) as avg_creator_likes,
  ROUND(AVG("Creator Video Count")) as avg_creator_videos
FROM sheet1
WHERE "Rank" >= 90;

-- S23
SELECT 
  "Main Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / 520, 1) as top10_pct,
  SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) as top30_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) / 1560, 1) as top30_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Main Category"
ORDER BY top10_count DESC;

-- S24
SELECT 
  "Video Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / COUNT(*), 1) as top10_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
HAVING COUNT(*) >= 15
ORDER BY top10_pct DESC
LIMIT 20;

-- S25
SELECT SUBSTR(_id, 1, 8) as id_prefix, COUNT(*) as cnt FROM sheet1 GROUP BY SUBSTR(_id, 1, 8) ORDER BY cnt DESC;

-- S26
SELECT COUNT(*) as total, COUNT(DISTINCT "Creator") as distinct_creators, COUNT(DISTINCT "Title") as distinct_titles, COUNT(DISTINCT "Video Category") as distinct_categories FROM sheet1;

-- S27
SELECT SUBSTR(_id, 1, 4) as id_prefix, COUNT(*) as cnt FROM sheet1 GROUP BY SUBSTR(_id, 1, 4) ORDER BY cnt DESC;

-- S28
SELECT 
  "Creator Video Count",
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Creator Video Count"
HAVING cnt >= 10
ORDER BY "Creator Video Count";

-- S29
SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 10
ORDER BY avg_rank ASC
LIMIT 20;

-- S30
SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 5
ORDER BY avg_views DESC
LIMIT 20;

-- S31
SELECT 
  CASE 
    WHEN "Creator Followers" < 10000 THEN '1. <10k'
    WHEN "Creator Followers" < 100000 THEN '2. 10k-100k'
    WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M'
    ELSE '4. >1M' 
  END as follower_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Coins")) as avg_coins
FROM sheet1
GROUP BY follower_band
ORDER BY follower_band;

-- S32
SELECT 
  CASE 
    WHEN "Creator Video Count" = 100 THEN '100 (full)'
    WHEN "Creator Video Count" < 10 THEN '1-9'
    WHEN "Creator Video Count" < 50 THEN '10-49'
    ELSE '50-99'
  END as video_count_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY video_count_band
ORDER BY video_count_band;

-- S33
SELECT 
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_5m,
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_2m
FROM sheet1;

-- S34
SELECT 
  "Video Category",
  COUNT(*) as cnt,
  ROUND(100.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_viral_2m,
  ROUND(AVG("Views")) as avg_views
FROM sheet1
GROUP BY "Video Category"
HAVING cnt >= 15
ORDER BY pct_viral_2m DESC
LIMIT 15;

-- S35
SELECT * FROM sheet1 WHERE Views >= 5000000 ORDER BY Views DESC;

-- S36
SELECT * FROM sheet1;

-- S37
SELECT "Main Category", COUNT(*) as cnt, MIN("Rank") as min_rank, MAX("Rank") as max_rank, COUNT(DISTINCT "Rank") as distinct_ranks
FROM sheet1
GROUP BY "Main Category"
ORDER BY cnt DESC;

-- S38
SELECT COUNT(*) as cnt, COUNT(DISTINCT "Title" || '|' || "Creator") as unique_videos FROM sheet1;

-- S39
SELECT _id, "Main Category", "Rank" FROM sheet1;

-- S40
SELECT * FROM sheet1;

-- S41
SELECT * FROM sheet1;

-- S42
SELECT * FROM sheet1;

-- S43
SELECT * FROM sheet1;

-- S44
SELECT * FROM sheet1;

-- S45
SELECT * FROM sheet1;

-- S46
SELECT * FROM sheet1;

-- S47
SELECT * FROM sheet1;

-- S48
SELECT * FROM sheet1;

-- S49
SELECT * FROM sheet1;

-- S50
SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as vstatus,
  COUNT(*) as cnt,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_2m,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_1m,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY vstatus;

-- S51
SELECT 
  "Video Category",
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Favorites")) as avg_fav,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku
FROM sheet1
WHERE "Main Category" = 'Whole site'
GROUP BY "Video Category"
HAVING COUNT(*) >= 3
ORDER BY avg_views DESC
LIMIT 15;



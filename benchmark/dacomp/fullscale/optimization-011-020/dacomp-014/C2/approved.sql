-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_014_c2" AS
SELECT "Video Category" AS __g0, "Main Category" AS __g1, "Creator Gender" AS __g2, CASE WHEN NOT "Bilibili Personal Verification" IS NULL THEN 'Verified' ELSE 'Not Verified' END AS __g3, "Creator Video Count" AS __g4, CASE WHEN "Rank" <= 10 THEN 'Top 10' WHEN "Rank" <= 30 THEN '11-30' WHEN "Rank" <= 50 THEN '31-50' WHEN "Rank" <= 70 THEN '51-70' ELSE '71-100' END AS __g5, SUBSTRING(_id, 1, 8) AS __g6, SUBSTRING(_id, 1, 4) AS __g7, "Creator" AS __g8, CASE WHEN "Creator Followers" < 10000 THEN '1. <10k' WHEN "Creator Followers" < 100000 THEN '2. 10k-100k' WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END AS __g9, CASE WHEN "Creator Video Count" = 100 THEN '100 (full)' WHEN "Creator Video Count" < 10 THEN '1-9' WHEN "Creator Video Count" < 50 THEN '10-49' ELSE '50-99' END AS __g10, COUNT(*) AS __a0, MIN("Rank") AS __a1, MAX("Rank") AS __a2, MIN("Views") AS __a3, SUM("Views") AS __a4_sum, COUNT("Views") AS __a4_n, MAX("Views") AS __a5, MIN("Likes") AS __a6, SUM("Likes") AS __a7_sum, COUNT("Likes") AS __a7_n, MAX("Likes") AS __a8, MIN("Coins") AS __a9, SUM("Coins") AS __a10_sum, COUNT("Coins") AS __a10_n, MAX("Coins") AS __a11, MIN("Favorites") AS __a12, SUM("Favorites") AS __a13_sum, COUNT("Favorites") AS __a13_n, MAX("Favorites") AS __a14, MIN("Shares") AS __a15, SUM("Shares") AS __a16_sum, COUNT("Shares") AS __a16_n, MAX("Shares") AS __a17, MIN("Comments") AS __a18, SUM("Comments") AS __a19_sum, COUNT("Comments") AS __a19_n, MAX("Comments") AS __a20, MIN("Danmaku Count") AS __a21, SUM("Danmaku Count") AS __a22_sum, COUNT("Danmaku Count") AS __a22_n, MAX("Danmaku Count") AS __a23, SUM("Overall Score") AS __a24_sum, COUNT("Overall Score") AS __a24_n, SUM("Rank") AS __a25_sum, COUNT("Rank") AS __a25_n, SUM("Creator Followers") AS __a26_sum, COUNT("Creator Followers") AS __a26_n, SUM("Creator Video Count") AS __a27_sum, COUNT("Creator Video Count") AS __a27_n, SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) AS __a28, SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) AS __a29, SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) AS __a30, SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) AS __a31, SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END) AS __a32 FROM "sheet1"  GROUP BY "Video Category", "Main Category", "Creator Gender", CASE WHEN NOT "Bilibili Personal Verification" IS NULL THEN 'Verified' ELSE 'Not Verified' END, "Creator Video Count", CASE WHEN "Rank" <= 10 THEN 'Top 10' WHEN "Rank" <= 30 THEN '11-30' WHEN "Rank" <= 50 THEN '31-50' WHEN "Rank" <= 70 THEN '51-70' ELSE '71-100' END, SUBSTRING(_id, 1, 8), SUBSTRING(_id, 1, 4), "Creator", CASE WHEN "Creator Followers" < 10000 THEN '1. <10k' WHEN "Creator Followers" < 100000 THEN '2. 10k-100k' WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END, CASE WHEN "Creator Video Count" = 100 THEN '100 (full)' WHEN "Creator Video Count" < 10 THEN '1-9' WHEN "Creator Video Count" < 50 THEN '10-49' ELSE '50-99' END;

-- S4
SELECT
  SUM(__a0) AS "total_rows"
FROM temp."reuse_014_c2";

-- S9
SELECT
  MIN(__a1) AS "min_rank",
  MAX(__a2) AS "max_rank"
FROM temp."reuse_014_c2";

-- S11
SELECT
  MIN(__a3) AS "min_views",
  (
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ) AS "avg_views",
  MAX(__a5) AS "max_views",
  MIN(__a6) AS "min_likes",
  (
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ) AS "avg_likes",
  MAX(__a8) AS "max_likes",
  MIN(__a9) AS "min_coins",
  (
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  ) AS "avg_coins",
  MAX(__a11) AS "max_coins",
  MIN(__a12) AS "min_fav",
  (
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  ) AS "avg_fav",
  MAX(__a14) AS "max_fav",
  MIN(__a15) AS "min_shares",
  (
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  ) AS "avg_shares",
  MAX(__a17) AS "max_shares",
  MIN(__a18) AS "min_comments",
  (
    1.0 * SUM(__a19_sum) / NULLIF(SUM(__a19_n), 0)
  ) AS "avg_comments",
  MAX(__a20) AS "max_comments",
  MIN(__a21) AS "min_danmaku",
  (
    1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
  ) AS "avg_danmaku",
  MAX(__a23) AS "max_danmaku"
FROM temp."reuse_014_c2";

-- S12
SELECT
  __g0 AS "Video Category",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a19_sum) / NULLIF(SUM(__a19_n), 0)
  )) AS "avg_comments",
  ROUND((
    1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
  )) AS "avg_danmaku",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score"
FROM temp."reuse_014_c2"
GROUP BY
  __g0
ORDER BY
  avg_views DESC
LIMIT 20;

-- S13
SELECT
  __g1 AS "Main Category",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank"
FROM temp."reuse_014_c2"
GROUP BY
  __g1
ORDER BY
  avg_views DESC;

-- S14
SELECT
  __g2 AS "Creator Gender",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers",
  ROUND((
    1.0 * SUM(__a27_sum) / NULLIF(SUM(__a27_n), 0)
  )) AS "avg_video_count"
FROM temp."reuse_014_c2"
GROUP BY
  __g2;

-- S15
SELECT
  __g3 AS "verification_status",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers"
FROM temp."reuse_014_c2"
GROUP BY
  __g3;

-- S16
SELECT
  __g4 AS "Creator Video Count",
  SUM(__a0) AS "count",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins",
  ROUND((
    1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
  )) AS "avg_favorites",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares"
FROM temp."reuse_014_c2"
GROUP BY
  __g4
ORDER BY
  __g4 DESC
LIMIT 20;

-- S19
SELECT
  __g5 AS "rank_band",
  __g1 AS "Main Category",
  SUM(__a0) AS "count"
FROM temp."reuse_014_c2"
GROUP BY
  __g5,
  __g1
ORDER BY
  rank_band,
  count DESC;

-- S23
SELECT
  __g1 AS "Main Category",
  SUM(__a0) AS "total_videos",
  SUM(__a28) AS "top10_count",
  ROUND(100.0 * SUM(__a28) / 520, 1) AS "top10_pct",
  SUM(__a29) AS "top30_count",
  ROUND(100.0 * SUM(__a29) / 1560, 1) AS "top30_pct",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score"
FROM temp."reuse_014_c2"
GROUP BY
  __g1
ORDER BY
  top10_count DESC;

-- S24
SELECT
  __g0 AS "Video Category",
  SUM(__a0) AS "total_videos",
  SUM(__a28) AS "top10_count",
  ROUND(100.0 * SUM(__a28) / SUM(__a0), 1) AS "top10_pct",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score"
FROM temp."reuse_014_c2"
GROUP BY
  __g0
HAVING
  SUM(__a0) >= 15
ORDER BY
  top10_pct DESC
LIMIT 20;

-- S25
SELECT
  __g6 AS "id_prefix",
  SUM(__a0) AS "cnt"
FROM temp."reuse_014_c2"
GROUP BY
  __g6
ORDER BY
  cnt DESC;

-- S27
SELECT
  __g7 AS "id_prefix",
  SUM(__a0) AS "cnt"
FROM temp."reuse_014_c2"
GROUP BY
  __g7
ORDER BY
  cnt DESC;

-- S29
SELECT
  __g8 AS "Creator",
  SUM(__a0) AS "num_videos_in_ranking",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers",
  ROUND((
    1.0 * SUM(__a27_sum) / NULLIF(SUM(__a27_n), 0)
  )) AS "avg_video_count"
FROM temp."reuse_014_c2"
GROUP BY
  __g8
HAVING
  SUM(__a0) >= 10
ORDER BY
  avg_rank ASC
LIMIT 20;

-- S30
SELECT
  __g8 AS "Creator",
  SUM(__a0) AS "num_videos_in_ranking",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a26_sum) / NULLIF(SUM(__a26_n), 0)
  )) AS "avg_followers",
  ROUND((
    1.0 * SUM(__a27_sum) / NULLIF(SUM(__a27_n), 0)
  )) AS "avg_video_count"
FROM temp."reuse_014_c2"
GROUP BY
  __g8
HAVING
  SUM(__a0) >= 5
ORDER BY
  avg_views DESC
LIMIT 20;

-- S31
SELECT
  __g9 AS "follower_band",
  SUM(__a0) AS "cnt",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  )) AS "avg_likes",
  ROUND((
    1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
  )) AS "avg_shares",
  ROUND((
    1.0 * SUM(__a10_sum) / NULLIF(SUM(__a10_n), 0)
  )) AS "avg_coins"
FROM temp."reuse_014_c2"
GROUP BY
  __g9
ORDER BY
  follower_band;

-- S32
SELECT
  __g10 AS "video_count_band",
  SUM(__a0) AS "cnt",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  )) AS "avg_views",
  ROUND((
    1.0 * SUM(__a24_sum) / NULLIF(SUM(__a24_n), 0)
  )) AS "avg_score",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank"
FROM temp."reuse_014_c2"
GROUP BY
  __g10
ORDER BY
  video_count_band;

-- S33
SELECT
  ROUND(1.0 * SUM(__a30) / SUM(__a0) * 100, 1) AS "pct_viral_5m",
  ROUND(1.0 * SUM(__a31) / SUM(__a0) * 100, 1) AS "pct_viral_2m"
FROM temp."reuse_014_c2";

-- S50
SELECT
  __g3 AS "vstatus",
  SUM(__a0) AS "cnt",
  ROUND(100.0 * SUM(__a31) / SUM(__a0), 1) AS "pct_viral_2m",
  ROUND(100.0 * SUM(__a32) / SUM(__a0), 1) AS "pct_viral_1m",
  ROUND((
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  )) AS "avg_rank"
FROM temp."reuse_014_c2"
GROUP BY
  __g3;

DROP TABLE temp."reuse_014_c2";

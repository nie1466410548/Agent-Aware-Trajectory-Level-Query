SELECT COUNT(*) AS total_reviews, SUM(rating) AS total_rating, AVG(rating) AS overall_avg_rating
FROM review
WHERE business_ref IN ('businessref_52','businessref_84','businessref_76','businessref_87','businessref_65','businessref_94','businessref_90','businessref_16');

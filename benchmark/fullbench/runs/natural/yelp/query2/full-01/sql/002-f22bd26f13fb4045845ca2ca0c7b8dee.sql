SELECT AVG(rating) AS avg_rating, COUNT(*) AS num_reviews
FROM review
WHERE business_ref IN ('businessid_10','businessid_11','businessid_24','businessid_30','businessid_4','businessid_46','businessid_47','businessid_64','businessid_96');


SELECT r.review_id, r.user_id, r.business_ref, r.date,
       CAST(regexp_extract(r.date, '((?:19|20)\d{2})', 1) AS INTEGER) AS yr
FROM review r
JOIN "user" u ON r.user_id = u.user_id
WHERE u.yelping_since LIKE '%2016%'

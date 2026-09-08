SELECT COUNT(DISTINCT business_ref) AS n_businesses_2018
FROM review
WHERE date >= '2018-01-01' AND date < '2019-01-01';

SELECT e."Treatment Barriers", COUNT(*) cnt
FROM encounters e
GROUP BY e."Treatment Barriers"
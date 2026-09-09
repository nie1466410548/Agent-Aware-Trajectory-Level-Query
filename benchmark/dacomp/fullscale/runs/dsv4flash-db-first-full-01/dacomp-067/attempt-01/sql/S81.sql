
SELECT scd.application_id,
       AVG(scd.rating) as avg_candidate_rating,
       COUNT(scd.scorecard_id) as num_scorecards
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
GROUP BY scd.application_id

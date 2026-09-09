SELECT o."Symptom improvement", COUNT(*) cnt
FROM treatmentoutcomes o
GROUP BY o."Symptom improvement"
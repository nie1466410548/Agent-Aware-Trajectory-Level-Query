
SELECT "Contact Location Type (Hospital/School/Mall)" AS loc, COUNT(*) AS n FROM epidemiological_investigation GROUP BY loc ORDER BY n DESC;
SELECT sample_path, COUNT(*) n FROM contents WHERE sample_path ILIKE '%readme%' GROUP BY sample_path ORDER BY n DESC LIMIT 30;

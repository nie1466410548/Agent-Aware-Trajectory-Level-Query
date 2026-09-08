SELECT DISTINCT repo_data_description FROM contents WHERE sample_path LIKE '%.swift' AND repo_data_description NOT LIKE '%non-binary%' LIMIT 20

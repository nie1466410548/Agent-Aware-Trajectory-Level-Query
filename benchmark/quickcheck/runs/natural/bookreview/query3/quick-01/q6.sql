SELECT MAX(CAST(SUBSTR(purchase_id, 12) AS INTEGER)) AS max_num, MIN(CAST(SUBSTR(purchase_id, 12) AS INTEGER)) AS min_num, COUNT(DISTINCT purchase_id) AS distinct_pid FROM review;

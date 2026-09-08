SELECT COUNT(*) AS total, SUM(CASE WHEN purchase_id LIKE 'bookid%' THEN 1 ELSE 0 END) AS bookid_style, SUM(CASE WHEN purchase_id LIKE 'purchaseid%' THEN 1 ELSE 0 END) AS purchaseid_style FROM review;

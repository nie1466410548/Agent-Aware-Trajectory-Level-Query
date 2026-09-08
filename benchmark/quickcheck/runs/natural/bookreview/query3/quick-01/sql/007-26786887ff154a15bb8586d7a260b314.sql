SELECT COUNT(*) AS total, MIN(book_id), MAX(book_id), SUM(CASE WHEN book_id LIKE 'purchaseid%' THEN 1 ELSE 0 END) AS pid_style FROM books_info;


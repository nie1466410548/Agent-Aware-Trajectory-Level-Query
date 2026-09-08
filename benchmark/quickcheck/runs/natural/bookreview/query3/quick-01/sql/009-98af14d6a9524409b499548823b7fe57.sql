SELECT MAX(CAST(SUBSTRING(book_id FROM 8) AS INTEGER)) AS max_num FROM books_info;


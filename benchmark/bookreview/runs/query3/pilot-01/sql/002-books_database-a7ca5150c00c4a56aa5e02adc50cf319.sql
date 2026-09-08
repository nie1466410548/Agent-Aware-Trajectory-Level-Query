SELECT book_id, title, categories FROM books_info WHERE categories LIKE '%Children%25%25' ESCAPE '!' LIMIT 5

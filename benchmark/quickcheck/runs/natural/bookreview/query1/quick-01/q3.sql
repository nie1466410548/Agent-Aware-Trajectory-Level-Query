SELECT book_id, details FROM books_info
WHERE substring(details from 'on [A-Z][a-z]+ \d{1,2}, (\d{4})') IS NULL;

SELECT MIN("Date") AS min_date, MAX("Date") AS max_date, COUNT(*) AS n_rows,
       COUNT(DISTINCT "Destination") AS n_dest
FROM sheet1
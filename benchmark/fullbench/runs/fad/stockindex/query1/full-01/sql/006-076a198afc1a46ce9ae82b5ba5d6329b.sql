SELECT Date, COUNT(*) c FROM index_trade WHERE Date NOT SIMILAR TO '[0-9]{4}-[0-9]{2}-[0-9]{2}.*' GROUP BY Date LIMIT 20

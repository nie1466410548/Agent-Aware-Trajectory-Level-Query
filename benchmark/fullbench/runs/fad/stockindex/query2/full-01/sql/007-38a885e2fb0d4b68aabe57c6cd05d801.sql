SELECT "Index", "Date", "Open", "Close" FROM index_trade WHERE "Index" IN ('NYA','IXIC','GSPTSE') AND ("Date" LIKE '%2018%' OR "Date" LIKE '%2017%')

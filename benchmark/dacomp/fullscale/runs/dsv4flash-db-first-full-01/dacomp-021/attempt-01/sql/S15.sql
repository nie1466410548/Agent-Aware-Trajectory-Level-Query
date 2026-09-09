WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key
  FROM sheet1
)
SELECT MIN(date_key) AS min_date, MAX(date_key) AS max_date, COUNT(DISTINCT date_key) AS days
FROM parsed
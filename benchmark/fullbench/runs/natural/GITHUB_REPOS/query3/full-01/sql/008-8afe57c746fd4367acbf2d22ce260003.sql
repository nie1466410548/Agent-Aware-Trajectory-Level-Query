SELECT COUNT(*) FROM languages WHERE lower(language_description) LIKE '%shell%' AND language_description NOT LIKE '%PowerShell%' AND language_description NOT LIKE '%Shell%'

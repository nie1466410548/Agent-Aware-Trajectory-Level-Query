SELECT Id, Name, Description FROM Product2 WHERE LOWER(Name) LIKE '%processing%' OR LOWER(Name) LIKE '%unit%' OR LOWER(Description) LIKE '%processing unit%'

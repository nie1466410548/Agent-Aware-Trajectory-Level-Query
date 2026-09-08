SELECT COUNT(*) AS bad FROM publicationinfo WHERE cpc IS NULL OR json_valid(cpc)=0

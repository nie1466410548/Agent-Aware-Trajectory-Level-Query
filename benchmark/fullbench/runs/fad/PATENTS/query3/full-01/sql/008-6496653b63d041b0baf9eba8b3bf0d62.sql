SELECT Patents_info, family_id FROM publicationinfo WHERE family_id IN (SELECT family_id FROM publicationinfo WHERE Patents_info LIKE 'UNIV CALIFORNIA%') ORDER BY family_id

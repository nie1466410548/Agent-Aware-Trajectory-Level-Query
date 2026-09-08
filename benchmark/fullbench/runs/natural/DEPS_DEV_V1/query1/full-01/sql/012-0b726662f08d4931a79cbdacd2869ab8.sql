SELECT RelationType, RelationProvenance, COUNT(*) AS n FROM project_packageversion WHERE System='NPM' GROUP BY 1,2 ORDER BY n DESC

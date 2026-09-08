SELECT RelationType, RelationProvenance, COUNT(*) c FROM project_packageversion GROUP BY 1,2 ORDER BY c DESC;


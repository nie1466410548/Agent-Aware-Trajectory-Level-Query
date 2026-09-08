SELECT RelationType, RelationProvenance,
       count(*) AS total,
       sum(CASE WHEN Name LIKE '%>%' THEN 1 ELSE 0 END) AS with_gt
FROM project_packageversion
WHERE System='NPM'
GROUP BY RelationType, RelationProvenance
ORDER BY total DESC

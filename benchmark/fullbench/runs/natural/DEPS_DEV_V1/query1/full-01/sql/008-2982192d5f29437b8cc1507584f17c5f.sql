SELECT (SELECT COUNT(*) FROM project_packageversion WHERE System='NPM') AS npm_links, (SELECT COUNT(*) FROM project_info) AS projects

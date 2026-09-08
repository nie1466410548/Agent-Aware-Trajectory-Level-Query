SELECT (SELECT COUNT(*) FROM project_packageversion WHERE System='NPM') AS ppv_npm,
       (SELECT COUNT(*) FROM project_packageversion) AS ppv_total,
       (SELECT COUNT(*) FROM project_info) AS info_total;

SELECT Name, Version, ProjectName, RelationType FROM project_packageversion
WHERE LOWER(ProjectName) IN ('lrembacz/vue-dragndrop','rrdelaney/reason','wizards-lab/routing');

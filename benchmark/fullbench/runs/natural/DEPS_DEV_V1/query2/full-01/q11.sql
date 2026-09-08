SELECT Name, Version, RelationType, RelationProvenance FROM project_packageversion
WHERE ProjectName IN ('mui-org/material-ui','moment/moment','lodash/lodash','semantic-org/semantic-ui','react-native-elements/react-native-elements')
LIMIT 40;

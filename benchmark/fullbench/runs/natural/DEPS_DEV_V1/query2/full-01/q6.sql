SELECT COUNT(*) AS mit_release_cnt FROM packageinfo
WHERE System='NPM' AND Licenses LIKE '%"MIT"%' AND VersionInfo LIKE '%"IsRelease": true%';

SELECT Name, Version, json_extract(VersionInfo,'$.Ordinal') AS ord
FROM (
  SELECT Name, Version, VersionInfo,
         ROW_NUMBER() OVER (PARTITION BY Name ORDER BY json_extract(VersionInfo,'$.Ordinal') DESC) AS rn
  FROM packageinfo
  WHERE System='NPM' AND json_extract(VersionInfo,'$.IsRelease') = 1
)
WHERE rn = 1


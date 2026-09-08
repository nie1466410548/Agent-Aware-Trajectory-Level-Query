SELECT Name, Version, json_extract(VersionInfo,'$.Ordinal') AS Ordinal FROM packageinfo WHERE System='NPM' AND json_extract(VersionInfo,'$.IsRelease') = 1

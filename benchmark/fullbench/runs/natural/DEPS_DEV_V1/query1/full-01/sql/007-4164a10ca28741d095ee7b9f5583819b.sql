SELECT COUNT(*) AS n, COUNT(DISTINCT Name) AS pkgs FROM packageinfo WHERE System='NPM'

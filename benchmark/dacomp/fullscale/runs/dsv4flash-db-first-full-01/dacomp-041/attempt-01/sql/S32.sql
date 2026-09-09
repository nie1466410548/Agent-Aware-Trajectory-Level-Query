
SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count", gi."Visitor Traffic",
       gi."Average Dwell Time (minutes)", gi."Surveillance Coverage Status", gi."Motion Detection Status",
       gi."Alarm System Status", gi."Access Control Status",
       dci."Airtightness", dci."Display case material", dci."Seal status", dci."Maintenance Status",
       dci."Filter status", dci."Silica gel status", dci."Humidity buffering capacity",
       dci."Pollutant absorption capacity", dci."Leak rate", dci."Pressure (Pa)",
       dci."Inert gas system status", dci."Fire suppression system status", dci."Power status", dci."Backup system status"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC

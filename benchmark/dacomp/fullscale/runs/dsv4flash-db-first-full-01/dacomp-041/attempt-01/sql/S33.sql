
SELECT gi."Daily Visitor Count" as dv,
       emd."Temperature (°C)" as temp, emd."Relative Humidity (%)" as rh
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")

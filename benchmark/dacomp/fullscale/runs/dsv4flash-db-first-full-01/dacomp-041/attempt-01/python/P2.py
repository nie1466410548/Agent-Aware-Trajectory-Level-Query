NB = '\xa0'
# Build query for high traffic halls using exact column names with nbsp
sql = f"""
SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       emd."Temperature (°C)", emd."24-hour Temperature Change", emd."Relative Humidity (%)", emd."24-hour Humidity Change",
       emd."Atmospheric Pressure (hPa)",
       aqr."Carbon dioxide concentration (ppm)", aqr."Total volatile organic compounds concentration (ppb)",
       aqr."Ozone concentration (ppb)", aqr."Sulfur dioxide concentration (ppb)", aqr."Nitrogen dioxide concentration (ppb)",
       aqr."PM2.5 concentration", aqr."PM10 concentration", aqr."Formaldehyde concentration",
       aqr."Air exchange rate", aqr."Airflow velocity (m/s)",
       lrr."{NB}Illuminance (Lux)", lrr."UV Irradiance (μW/cm²)", lrr."{NB}IR Irradiance (W/m²)", lrr."Visible Light Exposure (Lx·h)",
       spr."{NB}Vibration Level (mm/s²)", spr."{NB}Noise Level (dB)", spr."Dust Accumulation (mg/m²)",
       spr."{NB}Microbial Count (CFU)", spr."{NB}Mold Risk Index", spr."{NB}Pest Activity Level",
       spr."Metal Corrosion Rate", spr."Organic Degradation Index", spr."{NB}Color Change (ΔE)",
       spr."Surface Temperature (°C)", spr."Surface Relative Humidity (%)", spr."{NB}Condensation Risk",
       spr."Oxygen Concentration", spr."{NB}Nitrogen Concentration"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC
"""
r = db.query(sql)
print(r['executions'][0]['row_count'], r['executions'][0]['result_complete'])
df = db.frame(r)
print(df.shape)
print(df.head(10))
# Save for later use
df.to_csv('/work/high_traffic_env.csv', index=False)

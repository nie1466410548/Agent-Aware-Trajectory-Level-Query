NB = '\xa0'
# Get full population data for comparison
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
ORDER BY gi."Daily Visitor Count" DESC
"""
r = db.query(sql)
print(r['executions'][0]['row_count'])
df_all = db.frame(r)
print(df_all.shape)
df_all.to_csv('/work/all_env.csv', index=False)

# Artifact data for all
sql2 = f"""
SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       TRIM(acm."Preserve Cultural Relic Reference") as relic_ref,
       bai."Cultural Relic Name", bai."Dynasty", bai."Date (Year)", bai."Material Type", bai."Preservation Status",
       ar."Historical Significance Rating", ar."Research Value Rating", ar."Exhibition Value Rating",
       ar."Cultural Value Score", ar."Public Accessibility Rating", ar."Educational Value Rating",
       ar."Conservation Difficulty", ar."Treatment Complexity", ar."Material Stability", ar."Deterioration Rate",
       sd."Environmental Sensitivity", sd."Light Sensitivity", sd."Temperature Sensitivity", sd."Humidity Sensitivity",
       sd."Vibration Sensitivity", sd."Contamination Sensitivity",
       ca."Condition Assessment Rating",
       acm."Treatment Status", acm."Treatment Priority", acm."Treatment Effectiveness", acm."Reversibility Potential",
       sas."{NB}Security Level", sas."Insurance Value (USD)"
FROM gallery_information gi
JOIN artifact_conservation_and_maint acm ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
JOIN artifact_security_and_access sas ON TRIM(sas."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
ORDER BY gi."Daily Visitor Count" DESC
"""
r2 = db.query(sql2)
print(r2['executions'][0]['row_count'])
df_all_art = db.frame(r2)
print(df_all_art.shape)
df_all_art.to_csv('/work/all_artifacts.csv', index=False)
print("All data saved")
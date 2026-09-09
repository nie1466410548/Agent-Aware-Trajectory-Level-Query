import pandas as pd
import numpy as np

# Query via logged interface in Python, then convert to DataFrame
res = db.query("""SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID\"""")

rows = db.rows(res)
df = pd.DataFrame(rows)
print(df.shape)
print(df['origin'].value_counts())
print(df.dtypes.value_counts())

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Build DataFrame
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

execs = res['executions'][0]
rows = db.rows(res)
df = pd.DataFrame(rows, columns=execs['columns'])

# Convert dates
df['last_inbound'] = pd.to_datetime(df['last_inbound'])
df['last_outbound'] = pd.to_datetime(df['last_outbound'])
ref_date = pd.Timestamp('2024-12-31')

# Days since last inbound/outbound
df['days_since_inbound'] = (ref_date - df['last_inbound']).dt.days
df['days_since_outbound'] = (ref_date - df['last_outbound']).dt.days

# Calculate total stock
df['total_stock'] = df['qualified'] + df['near_expiry'] + df['quarantine']

# Stock-to-threshold ratio
df['stock_to_threshold'] = df['total_stock'] / df['max_threshold'].replace(0, 1)

# Parse discrepancy rate (mixed % and decimal formats)
def parse_disc_rate(val):
    if val is None:
        return 0.0
    val = str(val).strip()
    if val.endswith('%'):
        return float(val.replace('%', '')) / 100.0
    else:
        return float(val)

df['disc_rate_val'] = df['disc_rate'].apply(parse_disc_rate)

# Derived quality risk indicators
df['total_contamination'] = df['pest_mold'] + df['rodent'] + df['air_contam']
df['quality_issue_sum'] = (df['near_expiry'] + df['near_expiry2'] + df['expired'] + 
                           df['damaged'] + df['returned'] + df['total_contamination'] + 
                           df['temp_humidity'])

# Storage sensitivity: 1 if refrigerated, 0.5 if cool, 0 if room temp
df['storage_sensitivity'] = df['storage_condition'].map({
    'Refrigerated': 1.0, 'Cool': 0.5, 'Room temperature': 0.0
})

# Transport sensitivity: 1 if cold chain
df['transport_sensitivity'] = df['transport_mode'].map({'Cold-chain': 1.0, 'Land transport': 0.0}).fillna(0.0)

# GSP: 1 if not certified
df['gsp_risk'] = (df['gsp_status'] == 'Not certified').astype(float)

# Status flags
df['is_frozen'] = (df['inv_status'] == 'Frozen').astype(float)
df['is_scrapped'] = (df['inv_status'] == 'Scrapped').astype(float)
df['is_severe_alert'] = (df['alert_status'] == 'Severe').astype(float)
df['is_alert'] = (df['alert_status'] == 'Alert').astype(float)
df['zero_qualified'] = (df['qualified'] == 0).astype(float)
df['has_quarantine'] = (df['quarantine'] > 0).astype(float)

# ==========================================
# COMPOSITE SCORING
# ==========================================

# 1. INVENTORY BACKLOG SCORE (0-100)
# High stock relative to threshold, frozen/scrapped, stale (no movement)
# Normalize each component to 0-1 range using min-max or quantile clipping

# Stock ratio (log-transform to handle skew)
log_stock_ratio = np.log1p(df['stock_to_threshold'].clip(0, df['stock_to_threshold'].quantile(0.95)))
log_stock_norm = (log_stock_ratio - log_stock_ratio.min()) / (log_stock_ratio.max() - log_stock_ratio.min() + 1e-10)

# Days since outbound (stale stock)
outbound_days_norm = df['days_since_outbound'] / 365  # cap at 1 year

backlog_score = (
    log_stock_norm * 0.30 +
    df['is_frozen'] * 0.20 +
    df['is_scrapped'] * 0.15 +
    np.clip(outbound_days_norm, 0, 1) * 0.35
) * 100

# 2. SUPPLY INTERRUPTION SCORE (0-100)
# Zero qualified, frozen/scrapped, quarantine, days since inbound, alert status

inbound_days_norm = df['days_since_inbound'] / 365
supply_interrupt_score = (
    df['zero_qualified'] * 0.25 +
    df['is_frozen'] * 0.15 +
    df['is_scrapped'] * 0.10 +
    df['has_quarantine'] * 0.10 +
    df['is_severe_alert'] * 0.15 +
    df['is_alert'] * 0.05 +
    np.clip(inbound_days_norm, 0, 1) * 0.20
) * 100

# 3. QUALITY RISK SCORE (0-100)
# Expired, near-expiry, damaged, contamination, temp/humidity, storage sensitivity, GSP, discrepancy

# Log-transform quality issue sum
log_quality = np.log1p(df['quality_issue_sum'])
log_quality_norm = (log_quality - log_quality.min()) / (log_quality.max() - log_quality.min() + 1e-10)

# Discrepancy rate
disc_norm = df['disc_rate_val'] / df['disc_rate_val'].quantile(0.95).clip(0.001)

quality_score = (
    log_quality_norm * 0.35 +
    df['storage_sensitivity'] * 0.10 +
    df['transport_sensitivity'] * 0.05 +
    df['gsp_risk'] * 0.15 +
    np.clip(disc_norm, 0, 1) * 0.15 +
    np.clip(df['temp_humidity'] / 5, 0, 1) * 0.20
) * 100

# 4. OVERALL PRIORITY SCORE (weighted average)
df['backlog_score'] = backlog_score.round(1)
df['supply_interrupt_score'] = supply_interrupt_score.round(1)
df['quality_risk_score'] = quality_score.round(1)
df['priority_score'] = (backlog_score * 0.35 + supply_interrupt_score * 0.30 + quality_score * 0.35).round(1)

# Print summary
print("=== SCORE SUMMARY ===")
print(df[['origin', 'backlog_score', 'supply_interrupt_score', 'quality_risk_score', 'priority_score']].describe())

print("\n\n=== TOP 20 PRIORITY DRUGS (Imported/JV) ===")
top20 = df.nlargest(20, 'priority_score')
print(top20[['drug_id', 'origin', 'priority_score', 'backlog_score', 'supply_interrupt_score', 'quality_risk_score']].to_string(index=False))

# Save full results
df.to_csv('priority_scores.csv', index=False)
print("\n\nSaved to priority_scores.csv")
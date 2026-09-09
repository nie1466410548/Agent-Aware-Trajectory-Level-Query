import pandas as pd
import numpy as np

# Re-load all data with proper whitespace trimming
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
high_case = pd.read_csv('/work/high_traffic_cases.csv')

# Strip whitespace from string columns
for col in high_art.columns:
    if high_art[col].dtype == 'object':
        high_art[col] = high_art[col].str.strip()

for col in high_case.columns:
    if high_case[col].dtype == 'object':
        high_case[col] = high_case[col].str.strip()

# Now check
print("Treatment Priority:", high_art['Treatment Priority'].value_counts().to_dict())
print("Environmental Sensitivity:", high_art['Environmental Sensitivity'].value_counts().to_dict())
print("Vibration Sensitivity:", high_art['Vibration Sensitivity'].value_counts().to_dict())
print("Light Sensitivity:", high_art['Light Sensitivity'].value_counts().to_dict())
print("Preservation Status:", high_art['Preservation Status'].value_counts().to_dict())
print("Silica gel status:", high_case['Silica gel status'].value_counts().to_dict())
print("Maintenance Status:", high_case['Maintenance Status'].value_counts().to_dict())
print("Filter status:", high_case['Filter status'].value_counts().to_dict())
print("Seal status:", high_case['Seal status'].value_counts().to_dict())

# Now compute proper risk indicators
print("\n\n========== CORRECTED RISK INDICATORS ==========")
print(f"Treatment Priority - Urgent: {(high_art['Treatment Priority'] == 'Urgent').sum()}")
print(f"Treatment Priority - High: {(high_art['Treatment Priority'] == 'High').sum()}")
print(f"Rapid deterioration: {(high_art['Deterioration Rate'] == 'Rapid').sum()}")
print(f"Critical preservation: {(high_art['Preservation Status'] == 'Critical').sum()}")
print(f"High environmental sensitivity: {(high_art['Environmental Sensitivity'] == 'High').sum()}")
print(f"High vibration sensitivity: {(high_art['Vibration Sensitivity'] == 'High').sum()}")
print(f"High light sensitivity: {(high_art['Light Sensitivity'] == 'High').sum()}")
print(f"Poor seal status: {(high_case['Seal status'] == 'Poor').sum()}")
print(f"Filter Replace Now: {(high_case['Filter status'] == 'Replace Now').sum()}")
print(f"Silica gel Replace Now: {(high_case['Silica gel status'] == 'Replace Now').sum()}")
print(f"Maintenance Overdue: {(high_case['Maintenance Status'] == 'Overdue').sum()}")
print(f"Maintenance Due: {(high_case['Maintenance Status'] == 'Due').sum()}")

# Save corrected data
high_art.to_csv('/work/high_traffic_artifacts_clean.csv', index=False)
high_case.to_csv('/work/high_traffic_cases_clean.csv', index=False)
import pandas as pd
high_art = pd.read_csv('/work/high_traffic_artifacts.csv')
print("High art columns:")
print(high_art.columns.tolist())
print()
print("Treatment Priority unique values:", high_art['Treatment Priority'].unique())
print("Environmental Sensitivity unique:", high_art['Environmental Sensitivity'].unique())
print("Vibration Sensitivity unique:", high_art['Vibration Sensitivity'].unique())
print("Light Sensitivity unique:", high_art['Light Sensitivity'].unique())
print("Preservation Status unique:", high_art['Preservation Status'].unique())
print("Silica gel status unique:", high_case['Silica gel status'].unique())
print("Maintenance Status unique:", high_case['Maintenance Status'].unique())
print()
# Check for whitespace issues
for col in ['Treatment Priority', 'Environmental Sensitivity', 'Vibration Sensitivity', 'Light Sensitivity']:
    print(f"{col} values (repr):", [repr(v) for v in high_art[col].unique()])
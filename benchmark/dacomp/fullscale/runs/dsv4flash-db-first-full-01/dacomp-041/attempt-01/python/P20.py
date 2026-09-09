import pandas as pd
high_case = pd.read_csv('/work/high_traffic_cases.csv')
# Check raw values
print("Raw Maintenance Status values:")
for v in high_case['Maintenance Status'].unique():
    print(f"  [{v}] -> len={len(v)}")
print()
print("Raw Silica gel status values:")
for v in high_case['Silica gel status'].unique():
    print(f"  [{v}] -> len={len(v)}")
print()
print("Raw Filter status values:")
for v in high_case['Filter status'].unique():
    print(f"  [{v}] -> len={len(v)}")
print()
print("Raw Seal status values:")
for v in high_case['Seal status'].unique():
    print(f"  [{v}] -> len={len(v)}")
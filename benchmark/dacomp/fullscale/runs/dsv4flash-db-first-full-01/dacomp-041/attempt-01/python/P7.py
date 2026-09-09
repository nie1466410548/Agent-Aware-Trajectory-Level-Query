import pandas as pd
import numpy as np

# Load artifact data
df_all_art = pd.read_csv('/work/all_artifacts.csv')
high_art = df_all_art[df_all_art['Daily Visitor Count'] > 900].copy()
low_art = df_all_art[df_all_art['Daily Visitor Count'] <= 900].copy()

print(f"High-traffic artifacts: {len(high_art)}")
print(f"Low-traffic artifacts: {len(low_art)}")

# Compare artifact ratings
rating_cols = ['Historical Significance Rating', 'Research Value Rating', 'Exhibition Value Rating',
               'Cultural Value Score', 'Public Accessibility Rating', 'Educational Value Rating',
               'Condition Assessment Rating']

print("\n=== ARTIFACT RATINGS COMPARISON ===")
for col in rating_cols:
    h_mean = high_art[col].mean()
    l_mean = low_art[col].mean()
    print(f"{col}: High={h_mean:.2f}, Low={l_mean:.2f}, Diff={h_mean-l_mean:.2f}")

# Material type distribution
print("\n=== MATERIAL TYPE DISTRIBUTION ===")
print("High Traffic:")
print(high_art['Material Type'].value_counts())
print("\nLow Traffic:")
print(low_art['Material Type'].value_counts())

# Preservation Status
print("\n=== PRESERVATION STATUS ===")
print("High Traffic:")
print(high_art['Preservation Status'].value_counts())
print("\nLow Traffic:")
print(low_art['Preservation Status'].value_counts())

# Conservation Difficulty
print("\n=== CONSERVATION DIFFICULTY ===")
print("High Traffic:")
print(high_art['Conservation Difficulty'].value_counts())
print("\nLow Traffic:")
print(low_art['Conservation Difficulty'].value_counts())

# Deterioration Rate
print("\n=== DETERIORATION RATE ===")
print("High Traffic:")
print(high_art['Deterioration Rate'].value_counts())
print("\nLow Traffic:")
print(low_art['Deterioration Rate'].value_counts())

# Material Stability
print("\n=== MATERIAL STABILITY ===")
print("High Traffic:")
print(high_art['Material Stability'].value_counts())
print("\nLow Traffic:")
print(low_art['Material Stability'].value_counts())

# Sensitivity
print("\n=== ENVIRONMENTAL SENSITIVITY ===")
print("High Traffic:")
print(high_art['Environmental Sensitivity'].value_counts())
print("\nLow Traffic:")
print(low_art['Environmental Sensitivity'].value_counts())

# Treatment Status
print("\n=== TREATMENT STATUS ===")
print("High Traffic:")
print(high_art['Treatment Status'].value_counts())
print("\nLow Traffic:")
print(low_art['Treatment Status'].value_counts())

# Treatment Priority
print("\n=== TREATMENT PRIORITY ===")
print("High Traffic:")
print(high_art['Treatment Priority'].value_counts())
print("\nLow Traffic:")
print(low_art['Treatment Priority'].value_counts())

# Security Level
print("\n=== SECURITY LEVEL ===")
print("High Traffic:")
print(high_art['\xa0Security Level'].value_counts())
print("\nLow Traffic:")
print(low_art['\xa0Security Level'].value_counts())

# Insurance Value
print(f"\nAvg Insurance Value: High=${high_art['Insurance Value (USD)'].mean():.0f}, Low=${low_art['Insurance Value (USD)'].mean():.0f}")
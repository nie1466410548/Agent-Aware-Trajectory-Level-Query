import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Combine intermediate category data from S15 and S17
df1 = pd.read_json('/results/S15.rows.jsonl', lines=True)
df1.columns = ['Major_Category', 'Intermediate_Category', 'Sales_Month', 'Monthly_Amount', 'Monthly_Qty']
df2 = pd.read_json('/results/S17.rows.jsonl', lines=True)
df2.columns = ['Major_Category', 'Intermediate_Category', 'Sales_Month', 'Monthly_Amount', 'Monthly_Qty']
df = pd.concat([df1, df2], ignore_index=True)
df['Month'] = df['Sales_Month'].astype(str).str[4:6].astype(int)
df['Month_Label'] = df['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr'})

# For the remaining majors, print top intermediate trends
all_majors = sorted(df['Major_Category'].unique())
print("Majors covered:", all_majors)

print("\n=== Intermediate Category Trends (Top 3 per major, Jan vs Apr) ===")
for major in all_majors:
    cat_df = df[df['Major_Category'] == major].copy()
    top_inter = cat_df.groupby('Intermediate_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(3).index.tolist()
    print(f"\n{major}:")
    for inter in top_inter:
        inter_data = cat_df[cat_df['Intermediate_Category'] == inter].sort_values('Sales_Month')
        amounts = inter_data['Monthly_Amount'].values
        months = inter_data['Month_Label'].values
        if len(amounts) >= 2 and amounts[0] > 0:
            change = (amounts[-1] - amounts[0]) / amounts[0] * 100
            trend = "upward" if change > 10 else ("downward" if change < -10 else "stable")
            print(f"  {inter}: Jan={amounts[0]:.0f} Apr={amounts[-1]:.0f} | Change {change:+.1f}% ({trend})")
        elif len(amounts) >= 1:
            print(f"  {inter}: {dict(zip(months, amounts.round(0)))}")

# Unit price trends at major category level
print("\n\n=== Average Unit Price by Major Category and Month ===")

# Also look at daily patterns - check which days have high sales (Spring Festival around Feb 19 2015?)
res = db.query("""
SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"
""")
df_daily = db.frame(res)
df_daily['Date'] = pd.to_datetime(df_daily['Sales Date'].astype(str), format='%Y%m%d')
print("\nDaily data available:", len(df_daily))
print(df_daily.head(5))

# Find top days
print("\nTop 5 days by sales amount:")
print(df_daily.nlargest(5, 'total')[['Date','total','n']].to_string())
print("\nBottom 5 days:")
print(df_daily.nsmallest(5, 'total')[['Date','total','n']].to_string())
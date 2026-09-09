import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = [
 ["Department Store",64,1.6755,2.531,1692.9,47.11,0.8478,19.7,15.57,812783.0,25399.5,63,45140.0,716.5,0.547,0.375,0.391,0.3125,0.9708,32.08,0.515625],
 ["Food Store",63,1.632,2.703,681.8,48.22,0.8465,8.56,19.39,624432.0,20143.0,63,42460.0,674.0,0.46,0.349,0.317,0.3016,0.9766,32.66,0.50794],
 ["Restaurant",62,1.6164,2.257,734.1,47.15,0.8194,16.13,8.68,1089042.0,30251.2,62,41960.0,676.8,0.468,0.339,0.29,0.2903,0.9755,32.55,0.5],
 ["Gas station",60,1.6031,2.633,804.7,47.27,0.8467,19.57,14.91,1117258.0,31034.9,60,40000.0,666.7,0.483,0.333,0.333,0.25,0.9787,32.87,0.41667],
 ["Supermarket",59,1.5864,2.949,1567.4,46.27,0.8223,24.32,18.27,668702.0,22290.1,59,39260.0,665.4,0.458,0.407,0.271,0.2373,0.9724,32.24,0.44068],
 ["Shopping Center",58,1.529,2.68,1510.9,52.43,0.8418,11.02,12.91,583542.0,26524.6,57,42060.0,737.9,0.534,0.259,0.328,0.3448,0.9778,32.78,0.5],
 ["Retail Store",57,1.5206,2.183,636.8,55.81,0.8264,11.75,6.94,713517.0,25482.8,56,37920.0,677.1,0.526,0.263,0.421,0.3860,0.9793,32.93,0.43860],
 ["Specialty store",55,1.6459,2.869,1627.2,48.82,0.8615,13.96,7.76,960110.0,29094.2,55,30640.0,557.1,0.673,0.473,0.236,0.3636,0.9752,32.52,0.27273],
 ["Convenience Store",53,1.699,2.088,718.1,51.3,0.8363,18.51,19.78,841028.0,31149.2,51,37000.0,725.5,0.528,0.302,0.396,0.3585,0.9727,32.27,0.49057],
 ["Beverage Shop",52,1.565,2.494,692.7,45.0,0.8071,13.72,14.54,652482.0,31070.6,51,32420.0,635.7,0.423,0.333,0.333,0.4510,0.9818,33.18,0.5],
]
cols = ["Outlet Type","num_outlets","pos_target_ach","avg_vpo","avg_pc","avg_qual_rate",
        "avg_tar","avg_yoy","avg_mom","total_sales_value","avg_sales_value",
        "num_contracts","total_signing_amount","avg_signing_amount","renewal_ratio",
        "complaint_ratio","quality_ratio","renew_high_ratio","avg_pass_rate","avg_score","appeals_per_outlet"]
df = pd.DataFrame(data, columns=cols)

# Contract efficiency: total sales value per total signing amount
df["sales_per_signing_cny"] = df["total_sales_value"] / df["total_signing_amount"]
# Also sales value per outlet per contract
df = df.sort_values("sales_per_signing_cny", ascending=False)

fig, ax = plt.subplots(figsize=(13, 6))
colors = ["#2ecc71" if x > df["sales_per_signing_cny"].median() else "#e74c3c" for x in df["sales_per_signing_cny"]]
bars = ax.bar(df["Outlet Type"], df["sales_per_signing_cny"], color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)
for b, v in zip(bars, df["sales_per_signing_cny"]):
    ax.text(b.get_x() + b.get_width()/2, v, f'{v:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.axhline(df["sales_per_signing_cny"].median(), color='gray', linestyle='--', alpha=0.6, label=f'Median = {df["sales_per_signing_cny"].median():.2f}')
ax.set_xlabel("Outlet Type", fontweight='bold')
ax.set_ylabel("Sales Value per 1 CNY Contract Signing Amount", fontweight='bold')
ax.set_title("Contract Efficiency: Sales Generated per CNY of Contract Value by Outlet Type", fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig("/work/contract_efficiency.png", dpi=150)
plt.close()

print(df[["Outlet Type", "total_sales_value", "total_signing_amount", "sales_per_signing_cny"]].round(2).to_string(index=False))
print("saved contract_efficiency.png")
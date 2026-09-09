import numpy as np
import pandas as pd

result = db.query("""
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
""")
df = db.frame(result)

lm = df[df['is_low'] == 1].copy()
normal = df[df['is_low'] == 0]

lm['rev_per_unit'] = lm['Total Logistics Revenue'] / lm['Sales Quantity'].replace(0, 1)
lm['freight_per_unit'] = lm['Freight Cost'] / lm['Sales Quantity'].replace(0, 1)
lm['wh_per_unit'] = lm['Warehousing Cost'] / lm['Sales Quantity'].replace(0, 1)
lm['other_per_unit'] = lm['Other Operating Costs'] / lm['Sales Quantity'].replace(0, 1)
lm['discount_rate'] = lm['Discount Amount'] / lm['List Price Revenue'].replace(0, np.nan) * 100

print("=" * 80)
print("SCENARIO ANALYSIS FOR REMEDIES")
print("=" * 80)

# Reference values from normal orders
normal_freight_per_unit = (normal['Freight Cost'].sum() / normal['Sales Quantity'].sum())
normal_wh_per_unit = (normal['Warehousing Cost'].sum() / normal['Sales Quantity'].sum())
normal_other_per_unit = (normal['Other Operating Costs'].sum() / normal['Sales Quantity'].sum())
normal_rev_per_unit = (normal['Total Logistics Revenue'].sum() / normal['Sales Quantity'].sum())
normal_disc_rate = normal['Discount Amount'].sum() / normal['List Price Revenue'].sum() * 100

print(f"\nReference (Normal orders):")
print(f"  Freight per unit:    ${normal_freight_per_unit:.3f}")
print(f"  Warehousing per unit: ${normal_wh_per_unit:.3f}")
print(f"  Other per unit:       ${normal_other_per_unit:.3f}")
print(f"  Revenue per unit:     ${normal_rev_per_unit:.3f}")
print(f"  Discount rate:        {normal_disc_rate:.2f}%")

current_lm_profit = lm['Profit'].sum()
print(f"\nCurrent low-margin total profit: ${current_lm_profit:.2f}")

# Scenario 1: Cap discount rate at normal level (1.41%) - revenue uplift from recovering discount
# For low-margin orders, the discount is removed from List Price Revenue
lm['rev_wo_discount'] = lm['Total Logistics Revenue'] + lm['Discount Amount']
scen1_profit = lm['rev_wo_discount'].sum() - lm['Total Logistics Cost'].sum()
print(f"\nScenario 1 - Remove ALL discounts on low-margin orders (restore full List Price):")
print(f"  Current revenue:   ${lm['Total Logistics Revenue'].sum():.2f}")
print(f"  Potential revenue: ${lm['rev_wo_discount'].sum():.2f}")
print(f"  Potential profit:  ${scen1_profit:.2f} (vs current ${current_lm_profit:.2f})")

# Scenario 2: Moderate discount to normal average rate (1.41%)
# Estimate list price base: List Price Revenue (before discount)
lm['list_price'] = lm['List Price Revenue']
# Discount at normal rate would be list * 1.41%
lm['new_discount'] = lm['list_price'] * normal_disc_rate / 100
lm['new_rev'] = lm['list_price'] + lm['Logistics Value-Added Service Revenue'] - lm['new_discount']
# Note: Total Logistics Revenue = List Price Revenue - Discount + VAS? Let's check
# Total Logistics Revenue ~ List Price - Discount + VAS? Actually from data: rev = list - disc + vas
scen2_profit = lm['new_rev'].sum() - lm['Total Logistics Cost'].sum()
print(f"\nScenario 2 - Moderate discount to normal level ({normal_disc_rate:.2f}%):")
print(f"  Current discount total:  ${lm['Discount Amount'].sum():.2f}")
print(f"  New discount total:      ${lm['new_discount'].sum():.2f}")
print(f"  Recovered revenue:       ${lm['Discount Amount'].sum() - lm['new_discount'].sum():.2f}")
print(f"  Potential profit:        ${scen2_profit:.2f} (vs current ${current_lm_profit:.2f})")

# Scenario 3: Reduce freight/warehousing per-unit costs to normal levels
# Freight savings
lm['new_freight'] = lm['Sales Quantity'] * normal_freight_per_unit
lm['new_wh'] = lm['Sales Quantity'] * normal_wh_per_unit
lm['new_other'] = lm['Sales Quantity'] * normal_other_per_unit
freight_savings = (lm['Freight Cost'] - lm['new_freight']).sum()
wh_savings = (lm['Warehousing Cost'] - lm['new_wh']).sum()
other_savings = (lm['Other Operating Costs'] - lm['new_other']).sum()

scen3_profit = lm['Total Logistics Revenue'].sum() - (lm['new_freight'] + lm['new_wh'] + lm['new_other']).sum()
print(f"\nScenario 3 - Bring per-unit costs to normal levels:")
print(f"  Freight savings:     ${freight_savings:.2f}")
print(f"  Warehousing savings: ${wh_savings:.2f}")
print(f"  Other Op. savings:   ${other_savings:.2f}")
print(f"  Total cost savings:  ${freight_savings + wh_savings + other_savings:.2f}")
print(f"  Potential profit:    ${scen3_profit:.2f} (vs current ${current_lm_profit:.2f})")

# Scenario 4: Combined - moderate discount + cost savings (only on profitable orders)
print(f"\nScenario 4 - Combined (moderate discount + cost reduction):")
scen4_profit = scen2_profit  # cost stays same, revenue recovers
print(f"  From discount moderation: ${scen2_profit - current_lm_profit:.2f}")
print(f"  Combined potential:       ${scen2_profit + freight_savings + wh_savings + other_savings:.2f}")

# Scenario 5: Minimum order size policy
# What if we impose minimum order size of e.g. 5 units? Examine excluded orders
print(f"\nScenario 5 - Minimum Order Size Policy Analysis:")
for min_qty in [3, 4, 5, 6, 8]:
    below = lm[lm['Sales Quantity'] < min_qty]
    kept = lm[lm['Sales Quantity'] >= min_qty]
    print(f"  Min qty {min_qty}: excluded {len(below)} orders (losing ${below['Profit'].sum():.2f}), "
          f"remaining low-margin orders profit: ${kept['Profit'].sum():.2f}")

# Scenario 6: Raise revenue per unit to normal level
lm['new_rev_per_unit'] = normal_rev_per_unit
lm['new_total_rev'] = lm['Sales Quantity'] * normal_rev_per_unit
scen6_profit = lm['new_total_rev'].sum() - lm['Total Logistics Cost'].sum()
print(f"\nScenario 6 - Raise revenue per unit to normal level (${normal_rev_per_unit:.2f}):")
print(f"  Current revenue:      ${lm['Total Logistics Revenue'].sum():.2f}")
print(f"  Potential revenue:    ${lm['new_total_rev'].sum():.2f}")
print(f"  Potential profit:     ${scen6_profit:.2f}")

# Additional: quantify the quantity-discount interaction
print(f"\n--- Discount rate by quantity band (low-margin orders) ---")
lm['qty_band'] = pd.cut(lm['Sales Quantity'], bins=[0, 1, 2, 3, 4, 5, 6, 8, 10, 20, 100],
                        labels=['1', '2', '3', '4', '5', '6', '7-8', '9-10', '11-20', '21+'])
q = lm.groupby('qty_band', observed=True).agg(
    n=('Profit Margin', 'count'),
    avg_disc_rate=('discount_rate', 'mean'),
    total_profit=('Profit', 'sum')
).reset_index()
print(q.to_string(index=False))

print("\n=== SCENARIO ANALYSIS COMPLETE ===")
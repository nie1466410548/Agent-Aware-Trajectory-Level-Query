import pandas as pd
import numpy as np

merged = pd.read_pickle('/work/final_allocation.pkl')
geo = pd.read_pickle('/work/geo_seg.pkl')

print("=== FINAL BUDGET ALLOCATION TABLE ===")
print(f"{'App':30s} {'Budget':>10s} {'Share':>7s} {'ROI':>7s} {'SegA':>5s} {'SegB':>5s} {'TotRev':>8s} {'BCG':>15s} {'Priority':>10s}")
print("="*102)
for _, r in merged.iterrows():
    app = r['package_name'].ljust(30)
    bud = f"${r['allocated_budget']:,.0f}".rjust(10)
    shr = f"{r['budget_share']*100:.1f}%".rjust(7)
    roi = f"{r['expected_roi']:.1f}%".rjust(7)
    sa = str(int(r['segA_markets'])).rjust(5)
    sb = str(int(r['segB_markets'])).rjust(5)
    rev = f"${r['total_revenue_30d']:,.1f}".rjust(8)
    bcg = r['bcg_matrix_category'].rjust(15)
    pri = r['investment_priority'].rjust(10)
    print(f"{app} {bud} {shr} {roi} {sa} {sb} {rev} {bcg} {pri}")

print(f"\nTotal: ${merged['allocated_budget'].sum():,.0f}")
print(f"Portfolio expected ROI: {(merged['expected_inc_rev'].sum()-5_000_000)/5_000_000*100:.1f}%")

# Detailed segment A markets
print("\n=== SEGMENT A (High Conversion > 15% AND Low Revenue < $5) ===")
seg_a = geo[geo['segment'] == 'A']
for _, r in seg_a.iterrows():
    print(f"  {r['package_name']:30s} {r['country']:4s} {r['country_name']:20s} Conv={r['store_conversion_rate']:.2f}% Rev=${r['avg_daily_revenue']:.2f}/day Vis={r['store_visitors_30d']:,.0f}")

print("\n=== SEGMENT B (High Revenue > $7 AND Low Conversion < 10%) ===")
seg_b = geo[geo['segment'] == 'B']
for _, r in seg_b.iterrows():
    print(f"  {r['package_name']:30s} {r['country']:4s} {r['country_name']:20s} Rev=${r['avg_daily_revenue']:.2f}/day Conv={r['store_conversion_rate']:.2f}% Vis={r['store_visitors_30d']:,.0f}")

# Verify file existence
import os
for f in ['fig1_market_segmentation.png', 'fig2_budget_allocation.png', 'fig3_expected_roi.png']:
    path = f'/work/{f}'
    print(f"\n{f}: {'EXISTS' if os.path.exists(path) else 'MISSING'} ({os.path.getsize(path) if os.path.exists(path) else 0} bytes)")
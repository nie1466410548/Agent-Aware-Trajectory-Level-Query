import json
import pandas as pd
import numpy as np
import os

# Load the saved data
df = pd.read_csv('/work/final_risk_analysis.csv')

# Show top 15 priority accounts
print("TOP 15 PRIORITY ACCOUNTS FOR IMMEDIATE ACTION")
print("=" * 90)
top15 = df.nlargest(15, 'priority_score')[['account_name', 'industry_normalized', 'size_segment', 
                                            'annual_revenue', 'actual_contacts', 'chief_count', 
                                            'contact_density_ratio', 'decision_maker_ratio', 
                                            'dept_coverage', 'composite_risk', 'risk_category', 'priority_tier',
                                            'recommendations']]
for i, (_, r) in enumerate(top15.iterrows()):
    print(f"{i+1}. {r['account_name']} | {r['industry_normalized']} | {r['size_segment']} | ${r['annual_revenue']:,.0f}")
    print(f"   Contacts: {int(r['actual_contacts'])} | C-level: {int(r['chief_count'])} | CDR: {r['contact_density_ratio']:.1f} | DMR: {r['decision_maker_ratio']:.0f}% | Coverage: {int(r['dept_coverage'])}/5")
    print(f"   Risk: {r['composite_risk']:.1f} ({r['risk_category']}) | {r['priority_tier']}")
    print(f"   Action: {r['recommendations']}")
    print()

# Also show some accounts needing specific types of attention
print("\n" + "=" * 90)
print("ACCOUNTS WITH BEST PRACTICES (LOWEST RISK)")
print("=" * 90)
best = df.nsmallest(10, 'composite_risk')[['account_name', 'industry_normalized', 'annual_revenue', 
                                            'actual_contacts', 'contact_density_ratio', 
                                            'decision_maker_ratio', 'dept_coverage', 'composite_risk']]
for i, (_, r) in enumerate(best.iterrows()):
    print(f"{i+1}. {r['account_name']} | {r['industry_normalized']} | ${r['annual_revenue']:,.0f}")
    print(f"   Contacts: {int(r['actual_contacts'])} | CDR: {r['contact_density_ratio']:.1f} | DMR: {r['decision_maker_ratio']:.0f}% | Coverage: {int(r['dept_coverage'])}/5 | Risk: {r['composite_risk']:.1f}")

print("\n\nAnalysis complete. Ready for report generation.")
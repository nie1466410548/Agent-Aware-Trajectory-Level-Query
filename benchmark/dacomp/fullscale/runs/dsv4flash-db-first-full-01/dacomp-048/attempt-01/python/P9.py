import os
for f in ['salary_distribution.png', 'benefits_distribution.png', 'salary_factors.png', 'benefit_salary_impact.png']:
    path = f'/work/{f}'
    print(f"{f}: exists={os.path.exists(path)}, size={os.path.getsize(path) if os.path.exists(path) else 'N/A'}")

# Final summary numbers for the report
print("\n=== FINAL SUMMARY NUMBERS ===")
print("Total vocational school records: 9073")
print("With salary: 7936")
print("Clean salary records: 7933")
print("With benefits: 8055")
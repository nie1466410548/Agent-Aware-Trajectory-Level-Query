import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get address data for all customers (top countries)
res = db.query("""
  SELECT country, country_code, state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE country IS NOT NULL AND country != ''
  GROUP BY country
  ORDER BY customer_count DESC
  LIMIT 15
""")
top_countries = db.rows(res)
print("Top countries (by distinct customer360_id):")
for r in top_countries:
    print(f"  {r[0]}: {r[2]}")

# Get state data
res2 = db.query("""
  SELECT state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE state IS NOT NULL AND state != ''
  GROUP BY state
  ORDER BY customer_count DESC
  LIMIT 15
""")
top_states = db.rows(res2)
print("\nTop states (by distinct customer360_id):")
for r in top_states:
    print(f"  {r[0]}: {r[1]}")

# Create plot for top countries
plt.figure(figsize=(12, 6))
countries = [r[0] for r in top_countries][:10]
counts = [r[2] for r in top_countries][:10]
sns.barplot(x=counts, y=countries, palette='viridis')
plt.title('Top 10 Countries by Customer Count (All Addresses)', fontsize=14)
plt.xlabel('Distinct Customer IDs')
plt.tight_layout()
plt.savefig('/work/fig6_top_countries.png')
plt.close()

# Now let's also look at the cohort's demographics by customer_segment and lifecycle_stage
df = pd.read_csv('/work/cohort_data.csv')

# Segment x Lifecycle
plt.figure(figsize=(14, 8))
ct = pd.crosstab(df['customer_segment'], df['lifecycle_stage'])
sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
plt.title('Customer Segment × Lifecycle Stage (Cohort)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig7_segment_lifecycle.png')
plt.close()

# Health score distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['customer_health_score'], bins=30, kde=True)
plt.title('Customer Health Score Distribution (Cohort)', fontsize=14)
plt.xlabel('Health Score')
plt.tight_layout()
plt.savefig('/work/fig8_health_dist.png')
plt.close()

print("Additional figures saved")
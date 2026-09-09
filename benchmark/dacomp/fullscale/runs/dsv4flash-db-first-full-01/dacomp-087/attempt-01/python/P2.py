import json, pandas as pd, numpy as np

# Fix rep_df column names from S19
rep_df = pd.read_csv('/work/reps.csv', header=None)
rep_df.columns = ['owner_id', 'rep_name', 'manager_id', 'workload_score', 'efficiency_score', 
                  'num_customers', 'total_annual_revenue', 'coverage_rate_capped',
                  'distinct_states', 'distinct_cities', 'win_rate', 'avg_deal_size_usd', 
                  'avg_sales_cycle_days', 'opp_conversion_rate']
print("rep_df columns:", rep_df.columns.tolist())
print(rep_df.describe())

# Load customers
cust = pd.read_csv('/work/customers.csv')
print("\ncust columns:", cust.columns.tolist())
print(cust.describe())

# Check workload distribution
print("\nWorkload score stats:")
print(rep_df['workload_score'].describe())
print("\nStd vs 0.3*Avg:", rep_df['workload_score'].std(), "vs", 0.3*rep_df['workload_score'].mean())

# Efficiency score stats
print("\nEfficiency score stats:")
print(rep_df['efficiency_score'].describe())
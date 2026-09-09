import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Pull data from overview table
ov = db.query("""
SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
print("Overview shape:", ov_df.shape)
print("Columns:", ov_df.columns.tolist())
print(ov_df.head())

# Also pull performance table data for satisfaction proxy
pf = db.query("""
SELECT organization_id, organization_size_category, current_employee_count,
       avg_employee_satisfaction_proxy, high_achiever_percentage, avg_weekly_hours_per_employee
FROM workday__organization_performance
""")
pf_df = db.frame(pf)
print("Performance shape:", pf_df.shape)
print(pf_df.head())

# Merge on organization_id
ov_df = ov_df.merge(pf_df, on='organization_id', how='left', suffixes=('', '_perf'))
print("Merged shape:", ov_df.shape)
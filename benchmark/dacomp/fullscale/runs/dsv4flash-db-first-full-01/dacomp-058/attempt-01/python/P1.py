import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load campaign-level health scores
campaign_scores = pd.read_json('results/S30.rows.jsonl', lines=True)
print("All campaigns sorted by health score:")
print(campaign_scores[['campaign_id', 'campaign_name', 'campaign_type', 'bidding_strategy', 'industry', 'health_score', 'cost_eff', 'conv_quality', 'competitive', 'avg_monthly_cost', 'avg_roas']].to_string(index=False))

# Load monthly data
monthly = pd.read_json('results/S29.rows.jsonl', lines=True)
print("\n\nMonthly data shape:", monthly.shape)
print("Columns:", monthly.columns.tolist())
print("\nFirst few rows:")
print(monthly.head())
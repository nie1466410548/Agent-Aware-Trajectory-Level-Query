import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load 2024 data
rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)

# Compute correlations
corr_cols = ['Churn Rate', 'Level Rating', 'Clear Rate', 'Average Retry Count']
corr_matrix = df[corr_cols].corr()
print("Correlation Matrix:")
print(corr_matrix)
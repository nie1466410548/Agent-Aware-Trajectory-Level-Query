import pandas as pd
df = pd.read_csv('/work/customer_health_scores.csv')
print("Count health_score < 50:", (df['health_score'] < 50).sum())
print("Count health_score == 50:", (df['health_score'] == 50).sum())
print("Count health_score <= 50:", (df['health_score'] <= 50).sum())
print("Count health_score >= 80:", (df['health_score'] >= 80).sum())
print("Count health_score in [50,80):", ((df['health_score'] >= 50) & (df['health_score'] < 80)).sum())

# Exact boundary values
exact_vals = df['health_score'].value_counts().sort_index()
print("\nScores near boundaries:")
print(exact_vals[(exact_vals.index >= 48) & (exact_vals.index <= 51)])
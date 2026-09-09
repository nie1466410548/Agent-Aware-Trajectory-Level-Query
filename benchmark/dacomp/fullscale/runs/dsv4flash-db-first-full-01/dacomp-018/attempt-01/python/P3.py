import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/customer_profit_data.csv')
df['cart_rate'] = df['carts']/df['orders']
df['like_rate'] = df['likes']/df['orders']
df['share_rate'] = df['shares']/df['orders']
df['browse_per_order'] = df['browse_time']/df['orders']

# Define top 20% by profit
threshold = df['profit'].quantile(0.8)
top = df[df['profit'] >= threshold]
bottom = df[df['profit'] < threshold]
print(f'Top 20%: {len(top)} customers, Avg profit: ${top.profit.mean():.0f}')
print(f'Bottom 80%: {len(bottom)} customers, Avg profit: ${bottom.profit.mean():.0f}')
print(f'Top 20% female pct: {(top.gender=="Female").mean()*100:.1f}%')
print(f'Bottom 80% female pct: {(bottom.gender=="Female").mean()*100:.1f}%')

# Compare top vs bottom by gender
for g in ['Female','Male']:
    top_g = top[top.gender==g]
    bot_g = bottom[bottom.gender==g]
    print(f'\n{g} - Top20%: {len(top_g)} customers, avg_profit=${top_g.profit.mean():.0f}, avg_orders={top_g.orders.mean():.0f}, avg_cart_rate={top_g.cart_rate.mean():.3f}')
    print(f'{g} - Bottom80%: {len(bot_g)} customers, avg_profit=${bot_g.profit.mean():.0f}, avg_orders={bot_g.orders.mean():.0f}, avg_cart_rate={bot_g.cart_rate.mean():.3f}')

# Cohort analysis: segment composition of top customers
print('\n--- Top 20% customers ---')
print(pd.crosstab(top.gender, top.segment, margins=True))
print('\n--- Bottom 80% customers ---')
print(pd.crosstab(bottom.gender, bottom.segment, margins=True))

# What percentage of top customers are female?
print(f'\nTop 20% gender breakdown:')
print(top.gender.value_counts(normalize=True).mul(100).round(1))
print(f'\nFemale customers in top 20%: {(top.gender=="Female").sum()} / {top.shape[0]} = {(top.gender=="Female").mean()*100:.1f}%')
print(f'Female customers overall: {(df.gender=="Female").mean()*100:.1f}%')
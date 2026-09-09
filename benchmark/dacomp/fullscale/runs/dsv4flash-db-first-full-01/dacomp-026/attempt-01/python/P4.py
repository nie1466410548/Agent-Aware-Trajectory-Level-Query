import pandas as pd
df = pd.read_csv('/work/l5_dataset.csv')
print("costbene stats:", df['costbene'].describe())
print("budget stats:", df['budget'].describe())
print("costbene/budget ratio stats:", (df['costbene']/df['budget']).describe())
print("costbene/affected:", (df['costbene']/df['affected']).describe())
print("Correlation costbene ~ budget:", df[['costbene','budget']].corr().iloc[0,1])
print("Correlation costbene ~ affected:", df[['costbene','affected']].corr().iloc[0,1])

# Check if costbene is actually benefit-cost ratio (benefit per dollar)
# Since values range 13-980 and budgets ~5M, costbene/budget = 0.0001 roughly
# Could be net benefit in USD per $1000? costbene*1000/budget mean:
print("costbene*1000/budget:", (df['costbene']*1000/df['budget']).describe())

# Top and bottom 10 by delivery success
top = df.nlargest(10, 'deliv_success')[['Disaster Event ID','deliv_success','staff_total','budget','transport_vol','dist_points','deliv_time']]
bottom = df.nsmallest(10, 'deliv_success')[['Disaster Event ID','deliv_success','staff_total','budget','transport_vol','dist_points','deliv_time']]
print("\nTop 10 delivery success:")
print(top.to_string(index=False))
print("\nBottom 10 delivery success:")
print(bottom.to_string(index=False))
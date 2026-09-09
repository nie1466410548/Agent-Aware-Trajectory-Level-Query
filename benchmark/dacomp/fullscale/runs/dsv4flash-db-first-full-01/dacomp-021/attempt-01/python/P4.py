# Final summary statistics for the report
import numpy as np, pandas as pd

hourly = pd.read_csv('/work/hourly_stats.csv')
daily = pd.read_csv('/work/daily_stats.csv')
daily['date'] = pd.to_datetime(daily['date_key'])
daily['weekday'] = daily['date'].dt.dayofweek
daily['is_weekend'] = daily['weekday'].isin([5,6])
daily['cancel_pct'] = 100*daily['cancellations']/daily['bookings']

# Peak hours: 17-20 (evening), 9-11 (morning)
peak_evening = hourly[hourly['hour'].between(17,20)]
peak_morning = hourly[hourly['hour'].between(9,11)]
trough_night = hourly[hourly['hour'].between(0,4)]

print("=== PEAK/TROUGH METRICS ===")
for name, df in [('Evening peak (17-20)', peak_evening), ('Morning peak (9-11)', peak_morning), ('Night trough (0-4)', trough_night)]:
    tot = df['bookings'].sum()
    cancel = df['cancellations'].sum()
    nodrv = df['no_driver'].sum()
    inc = df['incomplete'].sum()
    comp = df['completed'].sum()
    cpk = np.average(df['cost_per_km'], weights=df['completed'])
    print(f"\n{name}:")
    print(f"  Total bookings: {tot} ({100*tot/150000:.1f}% of year)")
    print(f"  Cancel rate: {100*cancel/tot:.1f}%")
    print(f"  No driver rate: {100*nodrv/tot:.1f}%")
    print(f"  Incomplete rate: {100*inc/tot:.1f}%")
    print(f"  Avg cost/km: {cpk:.1f} ₹")

# Weekend vs weekday
w = daily[daily['is_weekend']]
nw = daily[~daily['is_weekend']]
print(f"\nWeekend avg cost/km: {w['cost_per_km'].mean():.2f} ₹")
print(f"Weekday avg cost/km: {nw['cost_per_km'].mean():.2f} ₹")
print(f"Weekend avg cancel: {w['cancel_pct'].mean():.2f}%")
print(f"Weekday avg cancel: {nw['cancel_pct'].mean():.2f}%")

# Top 3 peak days
top3 = daily.nlargest(3, 'bookings')
print("\nTop 3 peak days:")
for _, r in top3.iterrows():
    print(f"  {r['date_key']} ({r['date'].day_name()}): {r['bookings']} bookings, cancel {r['cancel_pct']:.1f}%, cost/km {r['cost_per_km']:.1f}₹")

# Bottom 3 trough days
bot3 = daily.nsmallest(3, 'bookings')
print("\nTop 3 trough days:")
for _, r in bot3.iterrows():
    print(f"  {r['date_key']} ({r['date'].day_name()}): {r['bookings']} bookings, cancel {r['cancel_pct']:.1f}%, cost/km {r['cost_per_km']:.1f}₹")

# 2024-01-26 is Republic Day in India
print("\n2024-01-26 (India Republic Day):",
      daily.loc[daily['date_key']=='2024-01-26', ['bookings','cancel_pct','cost_per_km']].to_string(index=False))
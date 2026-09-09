import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load data
result = db.query("""
SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Pickup Location", "Drop Location",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'
""")
df = db.frame(result)

# Average distance by vehicle type
print("Average ride distance by vehicle type:")
print(df.groupby('Vehicle Type')['Ride Distance'].mean().sort_values(ascending=False).round(2))

# Is there distance difference by vehicle type?
groups = [g['Ride Distance'].values for _, g in df.groupby('Vehicle Type')]
kw = stats.kruskal(*groups)
print(f"\nKruskal-Wallis Ride Distance by Vehicle Type: p={kw.pvalue:.4f}")

# Rating vs distance
print("\nAvg distance by rating band:")
df['rating_band'] = pd.cut(df['Driver Ratings'], bins=[3.0, 3.5, 4.0, 4.5, 5.0],
                           labels=['3.0-3.4', '3.5-3.9', '4.0-4.4', '4.5-5.0'])
print(df.groupby('rating_band', observed=True)['Ride Distance'].mean().round(2))

# Top locations by avg fare per km (with enough rides)
loc_stats = df.groupby('Pickup Location').agg(
    rides=('Booking Value', 'count'),
    avg_fare_per_km=('fare_per_km', 'mean'),
    avg_booking=('Booking Value', 'mean'),
    avg_distance=('Ride Distance', 'mean')
).reset_index()
loc_common = loc_stats[loc_stats['rides'] >= 300].sort_values('avg_fare_per_km', ascending=False)
print("\nTop 15 pickup locations by fare/km (>=300 rides):")
print(loc_common.head(15)[['Pickup Location', 'rides', 'avg_fare_per_km', 'avg_booking', 'avg_distance']].round(2))
print("\nBottom 10 pickup locations by fare/km (>=300 rides):")
print(loc_common.tail(10)[['Pickup Location', 'rides', 'avg_fare_per_km', 'avg_booking', 'avg_distance']].round(2))

# Distance bands: per-ride earning efficiency (revenue per km vs rides)
df['dist_band'] = pd.cut(df['Ride Distance'], bins=[0,5,10,15,20,25,30,40,100],
                         labels=['0-5','5-10','10-15','15-20','20-25','25-30','30-40','40+'])
dist_stats = df.groupby('dist_band', observed=True).agg(
    rides=('Booking Value', 'count'),
    avg_booking=('Booking Value', 'mean'),
    avg_fare_per_km=('fare_per_km', 'mean'),
    pct_weekend=('is_weekend', 'mean')
).reset_index() if 'is_weekend' in df.columns else None

# Recompute with weekend flag
df['is_weekend'] = df['day_of_week'].isin(['0', '6'])
dist_stats = df.groupby('dist_band', observed=True).agg(
    rides=('Booking Value', 'count'),
    avg_booking=('Booking Value', 'mean'),
    avg_fare_per_km=('fare_per_km', 'mean'),
    weekend_share=('is_weekend', 'mean')
).reset_index()
print("\nDistance band stats:")
print(dist_stats.round(2))

# Figure: distribution of booking values by vehicle type
plt.figure(figsize=(12, 5))
sns.boxplot(data=df.sample(20000), x='Vehicle Type', y='Booking Value', showfliers=False)
plt.title('Booking Value Distribution by Vehicle Type (sample of 20k)')
plt.ylabel('Booking Value (₹)')
plt.savefig('/work/fig6_booking_by_vehicle_box.png', dpi=100, bbox_inches='tight')
plt.close()

# Figure: weekend vs weekday hourly earnings potential
df['dow_label'] = np.where(df['is_weekend'], 'Weekend', 'Weekday')
hourly_dow = df.groupby(['hour', 'dow_label']).agg(
    avg_booking=('Booking Value', 'mean'),
    rides=('Booking Value', 'count')
).reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_dow, x='hour', y='avg_booking', hue='dow_label', marker='o')
plt.title('Average Booking Value by Hour: Weekend vs Weekday')
plt.xlabel('Hour of Day')
plt.ylabel('Avg Booking Value (₹)')
plt.grid(True, alpha=0.3)
plt.savefig('/work/fig7_weekend_vs_weekday_hourly.png', dpi=100, bbox_inches='tight')
plt.close()

print("\nSaved additional figures.")
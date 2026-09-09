import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load completed rides data
result = db.query("""
SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'
""")
df = db.frame(result)

# Correlation between Booking Value and Ride Distance
corr = df['Booking Value'].corr(df['Ride Distance'])
print(f"Correlation between Booking Value and Ride Distance: {corr:.4f}")

# Summary stats
print(f"\nBooking Value stats:")
print(df['Booking Value'].describe())
print(f"\nRide Distance stats:")
print(df['Ride Distance'].describe())
print(f"\nFare per km stats:")
print(df['fare_per_km'].describe())

# Figure 1: Booking Value vs Ride Distance scatter
plt.figure(figsize=(10, 6))
plt.scatter(df['Ride Distance'].sample(5000), df['Booking Value'].sample(5000), alpha=0.3, s=1)
plt.xlabel('Ride Distance (km)')
plt.ylabel('Booking Value (₹)')
plt.title(f'Booking Value vs Ride Distance (Corr: {corr:.3f})')
plt.grid(True, alpha=0.3)
plt.savefig('/work/fig1_booking_vs_distance.png', dpi=100, bbox_inches='tight')
plt.close()

# Figure 2: Average fare per km by vehicle type
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
vt_order = df.groupby('Vehicle Type')['fare_per_km'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Vehicle Type', y='fare_per_km', order=vt_order, ax=axes[0], ci=None, palette='viridis')
axes[0].set_title('Average Fare per km by Vehicle Type')
axes[0].set_xlabel('Vehicle Type')
axes[0].set_ylabel('Avg Fare per km (₹)')
axes[0].tick_params(axis='x', rotation=45)

vt_count = df.groupby('Vehicle Type').size().sort_values(ascending=False)
sns.barplot(x=vt_count.index, y=vt_count.values, ax=axes[1], palette='viridis')
axes[1].set_title('Completed Ride Count by Vehicle Type')
axes[1].set_xlabel('Vehicle Type')
axes[1].set_ylabel('Number of Completed Rides')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/fig2_vehicle_type_analysis.png', dpi=100, bbox_inches='tight')
plt.close()

# Figure 3: Day of week analysis
dow_map = {'0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', 
           '4': 'Thursday', '5': 'Friday', '6': 'Saturday'}
df['day_name'] = df['day_of_week'].map(dow_map)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
dow_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
sns.barplot(data=df, x='day_name', y='fare_per_km', order=dow_order, ax=axes[0], ci=None, palette='coolwarm')
axes[0].set_title('Average Fare per km by Day of Week')
axes[0].set_xlabel('Day of Week')
axes[0].set_ylabel('Avg Fare per km (₹)')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(data=df, x='day_name', y='Booking Value', order=dow_order, ax=axes[1], ci=None, palette='coolwarm')
axes[1].set_title('Average Booking Value by Day of Week')
axes[1].set_xlabel('Day of Week')
axes[1].set_ylabel('Avg Booking Value (₹)')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/fig3_day_of_week_analysis.png', dpi=100, bbox_inches='tight')
plt.close()

# Figure 4: Hourly analysis
hourly = df.groupby('hour').agg(
    avg_fare_per_km=('fare_per_km', 'mean'),
    avg_booking=('Booking Value', 'mean'),
    ride_count=('Booking Value', 'count')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))
color1 = 'tab:blue'
color2 = 'tab:orange'
ax1.bar(hourly['hour'], hourly['avg_fare_per_km'], alpha=0.7, color=color1, label='Avg Fare per km (₹)')
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Avg Fare per km (₹)', color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
ax2.plot(hourly['hour'], hourly['ride_count'], 'o-', color=color2, linewidth=2, label='Ride Count')
ax2.set_ylabel('Number of Rides', color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Hourly Analysis: Fare per km and Ride Volume')
fig.tight_layout()
plt.savefig('/work/fig4_hourly_analysis.png', dpi=100, bbox_inches='tight')
plt.close()

# Figure 5: Driver Rating distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(data=df, x='Driver Ratings', bins=20, ax=axes[0], kde=True, color='steelblue')
axes[0].set_title('Distribution of Driver Ratings')
axes[0].set_xlabel('Driver Ratings')
axes[0].set_ylabel('Count')

# Average fare per km by rating band
df['rating_band'] = pd.cut(df['Driver Ratings'], 
                           bins=[3.0, 3.5, 4.0, 4.5, 5.0],
                           labels=['3.0-3.4', '3.5-3.9', '4.0-4.4', '4.5-5.0'])
rating_analysis = df.groupby('rating_band').agg(
    avg_fare_per_km=('fare_per_km', 'mean'),
    avg_booking=('Booking Value', 'mean'),
    ride_count=('Booking Value', 'count')
).reset_index()
sns.barplot(data=rating_analysis, x='rating_band', y='avg_fare_per_km', ax=axes[1], palette='Blues_d')
axes[1].set_title('Average Fare per km by Driver Rating Band')
axes[1].set_xlabel('Driver Rating Band')
axes[1].set_ylabel('Avg Fare per km (₹)')

plt.tight_layout()
plt.savefig('/work/fig5_rating_analysis.png', dpi=100, bbox_inches='tight')
plt.close()

print("\nFigures saved successfully!")
print(f"\nTotal completed rides: {len(df)}")
print(f"Average fare per km: {df['fare_per_km'].mean():.2f}")
print(f"Average booking value: {df['Booking Value'].mean():.2f}")
print(f"Average ride distance: {df['Ride Distance'].mean():.2f}")
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = db.frame(db.query("""
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty
FROM health_education
WHERE "Population Covered" = 'Student'
"""))

df['behav_sig'] = (df['behav']=='Significant').astype(int)
df['track_sig'] = (df['track']=='Significant').astype(int)
df['eff_sig'] = (df['eff']=='Significant').astype(int)
df['both_sig'] = ((df['behav']=='Significant') & (df['track']=='Significant')).astype(int)

# Aggregate
agg = df.groupby(['format','location']).agg(
    n=('format','size'),
    behav_pct=('behav_sig', lambda x: round(100*x.mean(),1)),
    track_pct=('track_sig', lambda x: round(100*x.mean(),1)),
    eff_pct=('eff_sig', lambda x: round(100*x.mean(),1)),
    both_pct=('both_sig', lambda x: round(100*x.mean(),1)),
    both_n=('both_sig','sum')
).reset_index()

# Create a complex bubble chart
fig, ax = plt.subplots(figsize=(12, 8))

# Map formats to x positions and locations to colors
formats = ['Poster', 'Video', 'Lecture']
locations = ['Community', 'School', 'Hospital']
colors = {'Community': '#2ecc71', 'School': '#3498db', 'Hospital': '#e74c3c'}
markers = {'Poster': 'o', 'Video': 's', 'Lecture': '^'}

# Add jitter
np.random.seed(42)
for _, row in agg.iterrows():
    fmt = row['format']
    loc = row['location']
    x = formats.index(fmt) + np.random.uniform(-0.2, 0.2)
    y = locations.index(loc) + np.random.uniform(-0.2, 0.2)
    size = row['n'] * 80  # scale bubble size
    ax.scatter(x, y, s=size, c=colors[loc], alpha=0.7, edgecolors='black', linewidth=1.5, zorder=5)
    # Label with both_pct
    label = f"{row['both_pct']}%"
    if row['both_n'] > 0:
        label = f"{row['both_pct']}%\n({row['both_n']}/{row['n']})"
    ax.annotate(label, (x, y), ha='center', va='center', fontsize=9, fontweight='bold',
                color='black')

ax.set_xticks(range(len(formats)))
ax.set_xticklabels(formats, fontsize=12)
ax.set_yticks(range(len(locations)))
ax.set_yticklabels(locations, fontsize=12)
ax.set_xlabel('Campaign Format', fontsize=13)
ax.set_ylabel('Key Location', fontsize=13)
ax.set_title('Student Health Education Campaigns\nBubble Size = Number of Campaigns; Label = % Both Significant (Behavioral Change + Tracking)',
             fontsize=14, fontweight='bold')

# Add legend for bubble sizes
for s in [80, 400, 800, 1200]:
    ax.scatter([], [], s=s, c='gray', alpha=0.5, edgecolors='black', label=f'{s//80} campaigns')
ax.legend(loc='upper right', title='Sample Size', fontsize=9)

plt.tight_layout()
plt.savefig('/work/student_bubble_chart.png', dpi=150, bbox_inches='tight')
plt.close()

# Create a detailed bar chart of the top combos
top = agg.sort_values('both_pct', ascending=False).head(9)

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(top))
w = 0.2
ax.bar(x - 1.5*w, top['behav_pct'], w, label='Behavioral Change', color='#3498db')
ax.bar(x - 0.5*w, top['track_pct'], w, label='Effectiveness Tracking', color='#e67e22')
ax.bar(x + 0.5*w, top['eff_pct'], w, label='Effectiveness Assessment', color='#2ecc71')
ax.bar(x + 1.5*w, top['both_pct'], w, label='Both (Behavioral + Tracking)', color='#e74c3c')

ax.set_xticks(x)
labels = [f"{r['format']}\n@{r['location']}" for _, r in top.iterrows()]
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel('Percentage of Campaigns (%)', fontsize=12)
ax.set_title('Student Campaign Effectiveness by Format & Location', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper right')
ax.grid(axis='y', alpha=0.3)

# Add count annotations
for i, (_, r) in enumerate(top.iterrows()):
    ax.text(i, 1.5, f'n={r.n}', ha='center', fontsize=9, color='gray')

plt.tight_layout()
plt.savefig('/work/student_detailed_bar.png', dpi=150, bbox_inches='tight')
plt.close()

print("Saving final summary data...")
print(agg.to_string(index=False))
print("\n\nFigures saved: student_bubble_chart.png, student_detailed_bar.png")
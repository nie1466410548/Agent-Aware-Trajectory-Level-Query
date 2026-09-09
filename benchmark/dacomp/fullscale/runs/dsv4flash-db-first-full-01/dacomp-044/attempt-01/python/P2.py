import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get the aggregated data
agg = db.frame(db.query("""
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       COUNT(*) AS n,
       SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
       SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
       SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig,
       SUM(CASE WHEN "Effectiveness Assessment"='Significant' THEN 1 ELSE 0 END) AS eff_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location
"""))

agg['behav_pct'] = (agg['behav_sig']/agg['n']*100).round(1)
agg['track_pct'] = (agg['track_sig']/agg['n']*100).round(1)
agg['both_pct'] = (agg['both_sig']/agg['n']*100).round(1)
agg['eff_pct'] = (agg['eff_sig']/agg['n']*100).round(1)

# Pivot tables for heatmaps
pivot_behav = agg.pivot_table(index='format', columns='location', values='behav_pct', fill_value=0)
pivot_track = agg.pivot_table(index='format', columns='location', values='track_pct', fill_value=0)
pivot_both = agg.pivot_table(index='format', columns='location', values='both_pct', fill_value=0)
pivot_n = agg.pivot_table(index='format', columns='location', values='n', fill_value=0)

# Create heatmaps
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Health Education Campaign Effectiveness for Students\n(Percentage of Campaigns with Significant Outcomes)', fontsize=14, fontweight='bold')

sns.heatmap(pivot_behav, annot=True, fmt='.1f', cmap='YlGn', ax=axes[0,0], cbar_kws={'label': '% Significant'})
axes[0,0].set_title('Behavioral Change Assessment (Significant)')
axes[0,0].set_ylabel('Campaign Format')

sns.heatmap(pivot_track, annot=True, fmt='.1f', cmap='YlGn', ax=axes[0,1], cbar_kws={'label': '% Significant'})
axes[0,1].set_title('Effectiveness Tracking (Significant)')
axes[0,1].set_ylabel('Campaign Format')

sns.heatmap(pivot_both, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1,0], cbar_kws={'label': '% Both Significant'})
axes[1,0].set_title('Both: Behavioral Change + Effectiveness Tracking')
axes[1,0].set_ylabel('Campaign Format')

sns.heatmap(pivot_n, annot=True, fmt='.0f', cmap='Blues', ax=axes[1,1], cbar_kws={'label': 'Number of Campaigns'})
axes[1,1].set_title('Number of Student Campaigns (Sample Size)')
axes[1,1].set_ylabel('Campaign Format')

plt.tight_layout()
plt.savefig('/work/student_effectiveness_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Create grouped bar chart for the top combinations
top = agg.sort_values(['both_pct','n'], ascending=[False,False]).head(9)
top['combo'] = top['format'] + ' @ ' + top['location']

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(top))
w = 0.25
ax.bar(x - w, top['behav_pct'], w, label='Behavioral Change Significant', color='steelblue')
ax.bar(x, top['track_pct'], w, label='Effectiveness Tracking Significant', color='coral')
ax.bar(x + w, top['both_pct'], w, label='Both Significant', color='forestgreen')
ax.set_xticks(x)
ax.set_xticklabels(top['combo'], rotation=45, ha='right')
ax.set_ylabel('Percentage of Campaigns (%)')
ax.set_title('Campaign Effectiveness by Format & Location (Student Population)')
ax.legend()
ax.grid(axis='y', alpha=0.3)
for i, (_, row) in enumerate(top.iterrows()):
    ax.text(i, 1, f'n={row.n}', ha='center', fontsize=9, color='gray')
plt.tight_layout()
plt.savefig('/work/student_effectiveness_bar.png', dpi=150, bbox_inches='tight')
plt.close()

print("Visualizations saved.")
print("\nTop combinations by both_sig percentage:")
print(top[['format','location','n','behav_pct','track_pct','both_pct','eff_pct']].to_string(index=False))
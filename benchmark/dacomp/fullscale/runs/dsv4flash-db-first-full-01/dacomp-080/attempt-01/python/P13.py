import os
for f in ['fig1_score_distribution.png','fig2_tier_contribution.png','fig3_medium_vs_high.png',
          'fig4_lang_region_scores.png','fig5_tier_heatmap.png','fig6_score_decomposition.png',
          'fig7_cohort_trends.png','fig8_transition_by_region.png']:
    path = f'/work/{f}'
    print(f"{f}: {os.path.getsize(path)} bytes" if os.path.exists(path) else f"{f}: NOT FOUND")
import os
for f in ['figure1_monthly_value_trends.png','figure2_model_comparison.png','figure3_feature_importance.png','figure4_retention_by_decile.png']:
    print(f, os.path.exists('/work/'+f), os.path.getsize('/work/'+f) if os.path.exists('/work/'+f) else 0)
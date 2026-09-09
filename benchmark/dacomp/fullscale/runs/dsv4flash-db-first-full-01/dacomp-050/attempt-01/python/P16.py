import os
for f in ['student_suicidal_ideation_characteristics.png','student_predicted_probability_scenarios.png']:
    p = '/work/'+f
    print(f, os.path.getsize(p) if os.path.exists(p) else 'MISSING', 'bytes')

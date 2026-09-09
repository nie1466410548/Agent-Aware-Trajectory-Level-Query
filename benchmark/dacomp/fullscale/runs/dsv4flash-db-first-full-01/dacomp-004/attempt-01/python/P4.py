import os
# Check possible locations
for base in ['/data/nly/Agent-Aware-Trajectory-Level-Query', os.getcwd(), '/work']:
    print('BASE:', base, 'exists:', os.path.exists(base))
    if os.path.exists(base):
        for f in os.listdir(base)[:20]:
            print('   ', f)
        w = os.path.join(base, 'work')
        if os.path.exists(w):
            print('   /work contents:', os.listdir(w))

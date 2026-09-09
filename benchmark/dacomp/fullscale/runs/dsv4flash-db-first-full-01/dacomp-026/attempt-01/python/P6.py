import os
for f in sorted(os.listdir('/work')):
    print(f, os.path.getsize('/work/'+f))
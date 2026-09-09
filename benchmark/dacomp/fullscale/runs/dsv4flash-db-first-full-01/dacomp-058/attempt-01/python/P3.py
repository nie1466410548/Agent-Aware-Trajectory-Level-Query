import os
print("CWD:", os.getcwd())
print("Files in cwd:", os.listdir('.')[:20])
print("results dir exists:", os.path.exists('results'))
if os.path.exists('results'):
    print(os.listdir('results')[:10])
import glob
print("glob results:", glob.glob('**/S30*', recursive=True)[:5])
# Check db object availability
print("db type:", type(db).__name__)
print("db methods:", [m for m in dir(db) if not m.startswith('_')])
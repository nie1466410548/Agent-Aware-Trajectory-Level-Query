import os
print("CWD:", os.getcwd())
print("contents:", os.listdir('.'))
# Try to create work directory
try:
    os.makedirs('work', exist_ok=True)
    print("work dir created")
except:
    pass
# Check if we can write
print("cwd writable?", os.access('.', os.W_OK))
print("work dir exists:", os.path.exists('work'))
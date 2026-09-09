import os
print("CWD:", os.getcwd())
print("Contents:", os.listdir('.'))
# Check if work dir exists
if not os.path.exists('work'):
    os.makedirs('work')
    print("Created work directory")
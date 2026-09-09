import os
print("CWD:", os.getcwd())
print("Files in current dir:", [f for f in os.listdir('.') if f.endswith('.png') or f.endswith('.csv')])
print("Files in /work:", os.listdir('/work') if os.path.isdir('/work') else "/work not found")
print("Files in work/ (relative):", os.listdir('work') if os.path.isdir('work') else "work/ not found")
import os
print("CWD:", os.getcwd())
print("exists work:", os.path.isdir('work'))
print("contents:", os.listdir('.')[:20])
